from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User


class UserCRUD:
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        """
        Get a user by ID.
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get a user by email.
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """
        Get a user by username.
        """
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get a list of users with pagination.
        """
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, username: str, email: str, full_name: Optional[str] = None) -> User:
        """
        Create a new user.
        """
        user = User(username=username, email=email, full_name=full_name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def update_user(db: Session, user_id: int, **kwargs) -> Optional[User]:
        """
        Update a user's attributes.
        """
        user = UserCRUD.get_user(db, user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        Delete a user.
        """
        user = UserCRUD.get_user(db, user_id)
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        return True
