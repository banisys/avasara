from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func

from app.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)

    file_token = Column(String(255), unique=True, nullable=False)

    original_name = Column(String(255), nullable=False)

    extension = Column(String(20), nullable=False)

    text = Column(Text, nullable=True)

    status = Column(String(50), default="pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())