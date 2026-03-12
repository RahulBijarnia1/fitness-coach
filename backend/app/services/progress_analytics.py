"""
Advanced progress analytics service for FitCoach AI.

Provides comprehensive analysis of user progress including:
- Weight trend analysis
- Body composition tracking
- Goal progress estimation
- Calorie adherence analysis
- Weekly insights and recommendations
"""

from typing import Optional, List, Dict, Any
from datetime import date, timedelta
from dataclasses import dataclass
import math

from sqlalchemy.orm import Session

from app.repositories.progress_repository import ProgressRepository
from app.repositories.goal_repository import GoalRepository
from app.repositories.profile_repository import ProfileRepository
from app.core.logging import logger


@dataclass
class WeightTrend:
    """Weight trend analysis result."""
    direction: str  # "losing", "gaining", "stable"
    weekly_change: float  # kg per week
    total_change: float  # total kg changed
    consistency_score: float  # 0-100 based on entry frequency
    projected_weeks_to_goal: Optional[int]
    on_track: bool


@dataclass
class ProgressInsights:
    """Weekly progress insights."""
    current_weight: float
    starting_weight: float
    goal_weight: Optional[float]
    weight_change: float
    weight_change_pct: float
    body_fat_change: Optional[float]
    weekly_avg_weight: float
    trend: WeightTrend
    recommendations: List[str]
    achievements: List[str]


class ProgressAnalyticsService:
    """
    Service for analyzing user progress data.
    
    Provides advanced analytics including trend analysis,
    goal projections, and personalized insights.
    """
    
    # Constants for analysis
    IDEAL_WEEKLY_LOSS_KG = 0.45  # Healthy weight loss rate
    IDEAL_WEEKLY_GAIN_KG = 0.25  # Lean muscle gain rate
    STABLE_THRESHOLD_KG = 0.1   # Weight change threshold for "stable"
    MIN_ENTRIES_FOR_TREND = 3    # Minimum entries for trend analysis
    
    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
        self.progress_repo = ProgressRepository(db)
        self.goal_repo = GoalRepository(db)
        self.profile_repo = ProfileRepository(db)
    
    def get_weight_trend(
        self,
        user_id: int,
        days: int = 28,
    ) -> Optional[WeightTrend]:
        """
        Analyze weight trend over specified period.
        
        Args:
            user_id: User ID
            days: Number of days to analyze
            
        Returns:
            WeightTrend analysis or None if insufficient data
        """
        logs = self.progress_repo.get_recent_logs(user_id, days)
        
        if len(logs) < self.MIN_ENTRIES_FOR_TREND:
            logger.debug(f"Insufficient data for trend analysis: {len(logs)} entries")
            return None
        
        # Calculate weight change
        first_weight = logs[0].weight_kg
        last_weight = logs[-1].weight_kg
        total_change = last_weight - first_weight
        
        # Calculate weekly change rate
        days_elapsed = (logs[-1].log_date - logs[0].log_date).days
        weeks_elapsed = max(days_elapsed / 7, 1)
        weekly_change = total_change / weeks_elapsed
        
        # Determine trend direction
        if weekly_change < -self.STABLE_THRESHOLD_KG:
            direction = "losing"
        elif weekly_change > self.STABLE_THRESHOLD_KG:
            direction = "gaining"
        else:
            direction = "stable"
        
        # Calculate consistency score (based on entry frequency)
        expected_entries = days  # Ideally one entry per day
        actual_entries = len(logs)
        consistency_score = min(100, (actual_entries / expected_entries) * 100 * 3)
        
        # Get goal and calculate projection
        goal = self.goal_repo.get_by_user_id(user_id)
        projected_weeks = None
        on_track = True
        
        if goal and goal.target_weight:
            remaining = abs(goal.target_weight - last_weight)
            
            if direction == "losing" and goal.goal_type == "cut":
                projected_weeks = math.ceil(remaining / abs(weekly_change)) if weekly_change != 0 else None
                on_track = weekly_change < 0
            elif direction == "gaining" and goal.goal_type == "bulk":
                projected_weeks = math.ceil(remaining / weekly_change) if weekly_change != 0 else None
                on_track = weekly_change > 0
            elif goal.goal_type == "maintain":
                on_track = abs(weekly_change) < self.STABLE_THRESHOLD_KG
        
        return WeightTrend(
            direction=direction,
            weekly_change=round(weekly_change, 3),
            total_change=round(total_change, 2),
            consistency_score=round(consistency_score, 1),
            projected_weeks_to_goal=projected_weeks,
            on_track=on_track,
        )
    
    def get_body_fat_trend(
        self,
        user_id: int,
        days: int = 28,
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze body fat percentage trend.
        
        Args:
            user_id: User ID
            days: Number of days to analyze
            
        Returns:
            Body fat analysis or None
        """
        logs = self.progress_repo.get_recent_logs(user_id, days)
        bf_logs = [log for log in logs if log.body_fat_pct is not None]
        
        if len(bf_logs) < 2:
            return None
        
        first_bf = bf_logs[0].body_fat_pct
        last_bf = bf_logs[-1].body_fat_pct
        change = last_bf - first_bf
        
        # Calculate weekly change
        days_elapsed = (bf_logs[-1].log_date - bf_logs[0].log_date).days
        weeks_elapsed = max(days_elapsed / 7, 1)
        weekly_change = change / weeks_elapsed
        
        # Determine direction
        if weekly_change < -0.1:
            direction = "decreasing"
        elif weekly_change > 0.1:
            direction = "increasing"
        else:
            direction = "stable"
        
        return {
            "current_body_fat": round(last_bf, 1),
            "starting_body_fat": round(first_bf, 1),
            "total_change": round(change, 2),
            "weekly_change": round(weekly_change, 2),
            "direction": direction,
            "entries_count": len(bf_logs),
        }
    
    def estimate_calorie_adherence(
        self,
        user_id: int,
        days: int = 14,
    ) -> Optional[Dict[str, Any]]:
        """
        Estimate calorie adherence based on weight change.
        
        Uses the principle that ~7700 calories = 1kg of body weight
        to estimate if user is hitting their calorie targets.
        
        Args:
            user_id: User ID
            days: Number of days to analyze
            
        Returns:
            Calorie adherence estimation
        """
        CALORIES_PER_KG = 7700  # Approximate calories per kg
        
        logs = self.progress_repo.get_recent_logs(user_id, days)
        goal = self.goal_repo.get_by_user_id(user_id)
        
        if len(logs) < 2 or not goal:
            return None
        
        # Calculate actual weight change
        weight_change = logs[-1].weight_kg - logs[0].weight_kg
        days_elapsed = (logs[-1].log_date - logs[0].log_date).days or 1
        
        # Calculate expected weight change based on goal
        if goal.goal_type == "cut":
            expected_daily_deficit = 500  # Standard cut deficit
            expected_change = -(expected_daily_deficit * days_elapsed) / CALORIES_PER_KG
        elif goal.goal_type == "bulk":
            expected_daily_surplus = 350  # Standard bulk surplus
            expected_change = (expected_daily_surplus * days_elapsed) / CALORIES_PER_KG
        else:  # maintain
            expected_change = 0
        
        # Estimate adherence
        actual_calorie_balance = (weight_change * CALORIES_PER_KG) / days_elapsed
        
        if goal.goal_type == "cut":
            target_balance = -500
            adherence = 100 - min(100, abs(actual_calorie_balance - target_balance) / 5)
        elif goal.goal_type == "bulk":
            target_balance = 350
            adherence = 100 - min(100, abs(actual_calorie_balance - target_balance) / 3.5)
        else:
            target_balance = 0
            adherence = 100 - min(100, abs(actual_calorie_balance) / 2)
        
        return {
            "estimated_daily_balance": round(actual_calorie_balance),
            "target_daily_balance": target_balance,
            "adherence_score": round(max(0, adherence), 1),
            "on_target": adherence >= 70,
            "days_analyzed": days_elapsed,
            "assessment": self._get_adherence_assessment(adherence, goal.goal_type),
        }
    
    def _get_adherence_assessment(self, score: float, goal_type: str) -> str:
        """Get human-readable adherence assessment."""
        if score >= 90:
            return "Excellent! You're consistently hitting your targets."
        elif score >= 70:
            return "Good progress! Minor adjustments could optimize results."
        elif score >= 50:
            if goal_type == "cut":
                return "You may be eating above your target. Review portion sizes."
            elif goal_type == "bulk":
                return "You may need to increase food intake to hit surplus."
            else:
                return "Weight is fluctuating more than expected. Stay consistent."
        else:
            return "Consider reviewing your nutrition plan with your targets."
    
    def get_weekly_insights(self, user_id: int) -> Optional[ProgressInsights]:
        """
        Generate comprehensive weekly progress insights.
        
        Args:
            user_id: User ID
            
        Returns:
            ProgressInsights with recommendations
        """
        profile = self.profile_repo.get_by_user_id(user_id)
        goal = self.goal_repo.get_by_user_id(user_id)
        latest_log = self.progress_repo.get_latest_log(user_id)
        first_log = self.progress_repo.get_first_log(user_id)
        
        if not profile or not latest_log:
            return None
        
        # Get trend analysis
        trend = self.get_weight_trend(user_id, 28)
        
        # Get weekly averages
        weekly_avgs = self.progress_repo.get_weekly_averages(user_id, 4)
        current_week_avg = weekly_avgs[-1]["avg_weight"] if weekly_avgs else latest_log.weight_kg
        
        # Calculate changes
        starting_weight = first_log.weight_kg if first_log else profile.weight_kg
        weight_change = latest_log.weight_kg - starting_weight
        weight_change_pct = (weight_change / starting_weight) * 100
        
        # Body fat change
        bf_change = None
        if first_log and first_log.body_fat_pct and latest_log.body_fat_pct:
            bf_change = latest_log.body_fat_pct - first_log.body_fat_pct
        
        # Generate recommendations and achievements
        recommendations = self._generate_recommendations(trend, goal)
        achievements = self._generate_achievements(trend, weight_change, goal)
        
        return ProgressInsights(
            current_weight=latest_log.weight_kg,
            starting_weight=starting_weight,
            goal_weight=goal.target_weight if goal else None,
            weight_change=round(weight_change, 2),
            weight_change_pct=round(weight_change_pct, 2),
            body_fat_change=round(bf_change, 2) if bf_change else None,
            weekly_avg_weight=round(current_week_avg, 2),
            trend=trend,
            recommendations=recommendations,
            achievements=achievements,
        )
    
    def _generate_recommendations(
        self,
        trend: Optional[WeightTrend],
        goal: Any,
    ) -> List[str]:
        """Generate personalized recommendations based on progress."""
        recommendations = []
        
        if not trend:
            recommendations.append("Log your weight daily for personalized insights")
            return recommendations
        
        if trend.consistency_score < 50:
            recommendations.append("Try to log your weight more consistently for better tracking")
        
        if goal:
            if goal.goal_type == "cut":
                if trend.direction == "gaining":
                    recommendations.append("Consider reducing calorie intake or increasing activity")
                elif abs(trend.weekly_change) > self.IDEAL_WEEKLY_LOSS_KG * 1.5:
                    recommendations.append("You're losing weight quickly - ensure adequate nutrition")
                elif trend.on_track:
                    recommendations.append("Great progress! Maintain your current approach")
            
            elif goal.goal_type == "bulk":
                if trend.direction == "losing":
                    recommendations.append("Increase calorie intake to support muscle growth")
                elif trend.weekly_change > self.IDEAL_WEEKLY_GAIN_KG * 1.5:
                    recommendations.append("Gaining quickly - watch for excess fat gain")
                elif trend.on_track:
                    recommendations.append("Solid progress! Keep up the consistency")
            
            elif goal.goal_type == "maintain":
                if not trend.direction == "stable":
                    recommendations.append("Adjust calories slightly to maintain weight")
        
        # Add consistency recommendation if needed
        if not trend.on_track and trend.projected_weeks_to_goal:
            if trend.projected_weeks_to_goal > 52:
                recommendations.append("Consider adjusting your approach for faster results")
        
        return recommendations[:3]  # Limit to 3 recommendations
    
    def _generate_achievements(
        self,
        trend: Optional[WeightTrend],
        total_change: float,
        goal: Any,
    ) -> List[str]:
        """Generate achievements based on progress milestones."""
        achievements = []
        
        if trend and trend.consistency_score >= 80:
            achievements.append("🎯 Consistency Champion - Regular logging!")
        
        if goal:
            if goal.goal_type == "cut" and total_change <= -2:
                achievements.append(f"💪 Lost {abs(total_change):.1f}kg!")
            elif goal.goal_type == "bulk" and total_change >= 1:
                achievements.append(f"💪 Gained {total_change:.1f}kg!")
        
        if trend and trend.on_track:
            achievements.append("✅ On Track - Keep going!")
        
        return achievements
    
    def get_comprehensive_analytics(self, user_id: int) -> Dict[str, Any]:
        """
        Get all analytics in a single comprehensive response.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with all analytics data
        """
        insights = self.get_weekly_insights(user_id)
        weight_trend = self.get_weight_trend(user_id, 28)
        bf_trend = self.get_body_fat_trend(user_id, 28)
        calorie_adherence = self.estimate_calorie_adherence(user_id, 14)
        weekly_averages = self.progress_repo.get_weekly_averages(user_id, 8)
        weight_stats = self.progress_repo.get_weight_stats(user_id)
        
        return {
            "insights": {
                "current_weight": insights.current_weight if insights else None,
                "starting_weight": insights.starting_weight if insights else None,
                "goal_weight": insights.goal_weight if insights else None,
                "total_change": insights.weight_change if insights else None,
                "change_percentage": insights.weight_change_pct if insights else None,
                "recommendations": insights.recommendations if insights else [],
                "achievements": insights.achievements if insights else [],
            } if insights else None,
            "weight_trend": {
                "direction": weight_trend.direction,
                "weekly_change_kg": weight_trend.weekly_change,
                "total_change_kg": weight_trend.total_change,
                "consistency_score": weight_trend.consistency_score,
                "projected_weeks": weight_trend.projected_weeks_to_goal,
                "on_track": weight_trend.on_track,
            } if weight_trend else None,
            "body_fat_trend": bf_trend,
            "calorie_adherence": calorie_adherence,
            "weekly_averages": weekly_averages,
            "weight_stats": weight_stats,
        }
