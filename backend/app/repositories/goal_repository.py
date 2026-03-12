"""
Goal repository for database operations.
"""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.repositories.base_repository import BaseRepository


class GoalRepository(BaseRepository[Goal]):
    """
    Repository for Goal model operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(Goal, db)
    
    def get_by_user_id(self, user_id: int) -> Optional[Goal]:
        """
        Get goal by user ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Goal instance or None
        """
        return self.db.query(Goal).filter(Goal.user_id == user_id).first()
    
    def create_goal(
        self,
        user_id: int,
        goal_type: str,
        activity_level: str,
        calorie_target: int,
        protein_g: int,
        carbs_g: int,
        fat_g: int,
        timeline_weeks: Optional[int] = None,
        target_weight: Optional[float] = None,
    ) -> Goal:
        """
        Create a new fitness goal for a user.
        
        Args:
            user_id: User ID
            goal_type: Type of goal (cut/bulk/maintain)
            activity_level: Activity level
            calorie_target: Daily calorie target
            protein_g: Daily protein in grams
            carbs_g: Daily carbs in grams
            fat_g: Daily fat in grams
            timeline_weeks: Estimated weeks to reach goal
            target_weight: Target weight in kg
            
        Returns:
            Created Goal instance
        """
        return self.create({
            "user_id": user_id,
            "goal_type": goal_type,
            "activity_level": activity_level,
            "calorie_target": calorie_target,
            "protein_g": protein_g,
            "carbs_g": carbs_g,
            "fat_g": fat_g,
            "timeline_weeks": timeline_weeks,
            "target_weight": target_weight,
        })
    
    def update_goal(self, goal: Goal, **kwargs) -> Goal:
        """
        Update goal fields.
        
        Args:
            goal: Goal instance
            **kwargs: Fields to update
            
        Returns:
            Updated Goal instance
        """
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        return self.update(goal, update_data)
    
    def has_goal(self, user_id: int) -> bool:
        """
        Check if user has a goal set.
        
        Args:
            user_id: User ID
            
        Returns:
            True if goal exists
        """
        return self.db.query(
            self.db.query(Goal).filter(Goal.user_id == user_id).exists()
        ).scalar()
    
    def delete_user_goal(self, user_id: int) -> bool:
        """
        Delete user's goal.
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted
        """
        goal = self.get_by_user_id(user_id)
        if goal:
            return self.delete(goal)
        return False
