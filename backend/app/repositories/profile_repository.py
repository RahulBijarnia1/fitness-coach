"""
Profile repository for database operations.
"""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.repositories.base_repository import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
    """
    Repository for Profile model operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(Profile, db)
    
    def get_by_user_id(self, user_id: int) -> Optional[Profile]:
        """
        Get profile by user ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Profile instance or None
        """
        return self.db.query(Profile).filter(Profile.user_id == user_id).first()
    
    def create_profile(
        self,
        user_id: int,
        age: int,
        sex: str,
        height_cm: float,
        weight_kg: float,
        body_fat_pct: Optional[float] = None,
    ) -> Profile:
        """
        Create a new profile for a user.
        
        Args:
            user_id: User ID
            age: User age
            sex: User sex (M/F)
            height_cm: Height in centimeters
            weight_kg: Weight in kilograms
            body_fat_pct: Body fat percentage (optional)
            
        Returns:
            Created Profile instance
        """
        return self.create({
            "user_id": user_id,
            "age": age,
            "sex": sex,
            "height_cm": height_cm,
            "weight_kg": weight_kg,
            "body_fat_pct": body_fat_pct,
        })
    
    def update_profile(
        self,
        profile: Profile,
        **kwargs,
    ) -> Profile:
        """
        Update profile fields.
        
        Args:
            profile: Profile instance
            **kwargs: Fields to update
            
        Returns:
            Updated Profile instance
        """
        # Filter out None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}
        return self.update(profile, update_data)
    
    def has_profile(self, user_id: int) -> bool:
        """
        Check if user has a profile.
        
        Args:
            user_id: User ID
            
        Returns:
            True if profile exists
        """
        return self.db.query(
            self.db.query(Profile).filter(Profile.user_id == user_id).exists()
        ).scalar()
