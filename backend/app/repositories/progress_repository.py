"""
Progress repository for database operations.
"""

from typing import List, Optional, Tuple
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.models.progress import ProgressLog
from app.repositories.base_repository import BaseRepository


class ProgressRepository(BaseRepository[ProgressLog]):
    """
    Repository for ProgressLog model operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(ProgressLog, db)
    
    def get_user_logs(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
    ) -> List[ProgressLog]:
        """
        Get paginated progress logs for a user.
        
        Args:
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of ProgressLog instances
        """
        return (
            self.db.query(ProgressLog)
            .filter(ProgressLog.user_id == user_id)
            .order_by(desc(ProgressLog.log_date))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def count_user_logs(self, user_id: int) -> int:
        """
        Count total logs for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Total log count
        """
        return (
            self.db.query(func.count(ProgressLog.id))
            .filter(ProgressLog.user_id == user_id)
            .scalar()
        )
    
    def get_logs_in_range(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> List[ProgressLog]:
        """
        Get logs within a date range.
        
        Args:
            user_id: User ID
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            List of ProgressLog instances
        """
        return (
            self.db.query(ProgressLog)
            .filter(
                ProgressLog.user_id == user_id,
                ProgressLog.log_date >= start_date,
                ProgressLog.log_date <= end_date,
            )
            .order_by(ProgressLog.log_date)
            .all()
        )
    
    def get_recent_logs(
        self,
        user_id: int,
        days: int = 7,
    ) -> List[ProgressLog]:
        """
        Get logs from the past N days.
        
        Args:
            user_id: User ID
            days: Number of days to look back
            
        Returns:
            List of ProgressLog instances
        """
        cutoff_date = date.today() - timedelta(days=days)
        return (
            self.db.query(ProgressLog)
            .filter(
                ProgressLog.user_id == user_id,
                ProgressLog.log_date >= cutoff_date,
            )
            .order_by(ProgressLog.log_date)
            .all()
        )
    
    def get_latest_log(self, user_id: int) -> Optional[ProgressLog]:
        """
        Get the most recent log for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Most recent ProgressLog or None
        """
        return (
            self.db.query(ProgressLog)
            .filter(ProgressLog.user_id == user_id)
            .order_by(desc(ProgressLog.log_date))
            .first()
        )
    
    def get_first_log(self, user_id: int) -> Optional[ProgressLog]:
        """
        Get the first log for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            First ProgressLog or None
        """
        return (
            self.db.query(ProgressLog)
            .filter(ProgressLog.user_id == user_id)
            .order_by(ProgressLog.log_date)
            .first()
        )
    
    def create_log(
        self,
        user_id: int,
        weight_kg: float,
        body_fat_pct: Optional[float] = None,
        log_date: Optional[date] = None,
    ) -> ProgressLog:
        """
        Create a new progress log entry.
        
        Args:
            user_id: User ID
            weight_kg: Weight in kilograms
            body_fat_pct: Body fat percentage (optional)
            log_date: Log date (defaults to today)
            
        Returns:
            Created ProgressLog instance
        """
        return self.create({
            "user_id": user_id,
            "weight_kg": weight_kg,
            "body_fat_pct": body_fat_pct,
            "log_date": log_date or date.today(),
        })
    
    def get_weight_stats(self, user_id: int) -> dict:
        """
        Get weight statistics for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with min, max, avg weight
        """
        result = self.db.query(
            func.min(ProgressLog.weight_kg).label("min_weight"),
            func.max(ProgressLog.weight_kg).label("max_weight"),
            func.avg(ProgressLog.weight_kg).label("avg_weight"),
        ).filter(ProgressLog.user_id == user_id).first()
        
        return {
            "min_weight": float(result.min_weight) if result.min_weight else None,
            "max_weight": float(result.max_weight) if result.max_weight else None,
            "avg_weight": round(float(result.avg_weight), 2) if result.avg_weight else None,
        }
    
    def get_weekly_averages(
        self,
        user_id: int,
        weeks: int = 4,
    ) -> List[dict]:
        """
        Get weekly average weights.
        
        Args:
            user_id: User ID
            weeks: Number of weeks to analyze
            
        Returns:
            List of weekly averages
        """
        cutoff_date = date.today() - timedelta(weeks=weeks * 7)
        logs = self.get_logs_in_range(user_id, cutoff_date, date.today())
        
        if not logs:
            return []
        
        # Group by week
        weekly_data = {}
        for log in logs:
            week_start = log.log_date - timedelta(days=log.log_date.weekday())
            week_key = week_start.isoformat()
            
            if week_key not in weekly_data:
                weekly_data[week_key] = {"weights": [], "body_fats": []}
            
            weekly_data[week_key]["weights"].append(log.weight_kg)
            if log.body_fat_pct:
                weekly_data[week_key]["body_fats"].append(log.body_fat_pct)
        
        # Calculate averages
        result = []
        for week_start, data in sorted(weekly_data.items()):
            avg_weight = sum(data["weights"]) / len(data["weights"])
            avg_bf = (
                sum(data["body_fats"]) / len(data["body_fats"])
                if data["body_fats"]
                else None
            )
            result.append({
                "week_start": week_start,
                "avg_weight": round(avg_weight, 2),
                "avg_body_fat": round(avg_bf, 2) if avg_bf else None,
                "entries": len(data["weights"]),
            })
        
        return result
