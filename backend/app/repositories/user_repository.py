"""
User repository for database operations.
"""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Repository for User model operations.
    """
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            email: User email address
            
        Returns:
            User instance or None
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def email_exists(self, email: str) -> bool:
        """
        Check if email is already registered.
        
        Args:
            email: Email address to check
            
        Returns:
            True if email exists
        """
        return self.db.query(
            self.db.query(User).filter(User.email == email).exists()
        ).scalar()
    
    def create_user(self, email: str, password_hash: str) -> User:
        """
        Create a new user.
        
        Args:
            email: User email address
            password_hash: Hashed password
            
        Returns:
            Created User instance
        """
        return self.create({
            "email": email,
            "password_hash": password_hash
        })
    
    def update_password(self, user: User, new_password_hash: str) -> User:
        """
        Update user password.
        
        Args:
            user: User instance
            new_password_hash: New hashed password
            
        Returns:
            Updated User instance
        """
        return self.update(user, {"password_hash": new_password_hash})
