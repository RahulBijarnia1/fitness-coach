"""
Base repository class with common CRUD operations.

Provides a generic implementation for database operations that can be
extended by specific repositories.
"""

from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc

from app.config.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic repository with common CRUD operations.
    
    Attributes:
        model: SQLAlchemy model class
        db: Database session
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        Initialize repository with model and session.
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """
        Get a single record by ID.
        
        Args:
            id: Primary key value
            
        Returns:
            Model instance or None
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: Any = None,
        descending: bool = False,
    ) -> List[ModelType]:
        """
        Get all records with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            order_by: Column to order by
            descending: Order in descending order
            
        Returns:
            List of model instances
        """
        query = self.db.query(self.model)
        
        if order_by is not None:
            if descending:
                query = query.order_by(desc(order_by))
            else:
                query = query.order_by(order_by)
        
        return query.offset(skip).limit(limit).all()
    
    def count(self) -> int:
        """
        Count total number of records.
        
        Returns:
            Total record count
        """
        return self.db.query(func.count(self.model.id)).scalar()
    
    def create(self, obj_data: dict) -> ModelType:
        """
        Create a new record.
        
        Args:
            obj_data: Dictionary of field values
            
        Returns:
            Created model instance
        """
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, db_obj: ModelType, update_data: dict) -> ModelType:
        """
        Update an existing record.
        
        Args:
            db_obj: Model instance to update
            update_data: Dictionary of fields to update
            
        Returns:
            Updated model instance
        """
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def delete(self, db_obj: ModelType) -> bool:
        """
        Delete a record.
        
        Args:
            db_obj: Model instance to delete
            
        Returns:
            True if deleted successfully
        """
        self.db.delete(db_obj)
        self.db.commit()
        return True
    
    def exists(self, id: int) -> bool:
        """
        Check if a record exists.
        
        Args:
            id: Primary key value
            
        Returns:
            True if record exists
        """
        return self.db.query(
            self.db.query(self.model).filter(self.model.id == id).exists()
        ).scalar()
