from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True) # key for password login
    google_id = Column(String, unique=True, index=True, nullable=True) # key for google login
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
