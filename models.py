from sqlalchemy import Column, String, Integer, TIMESTAMP,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from database import Base
class Project(Base):
    __tablename__="projects"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    user_id=Column(UUID(as_uuid=True),nullable=False)
    doc_type=Column(String,nullable=False)
    topic=Column(String,nullable=False)
    created_at=Column(TIMESTAMP,server_default=func.now())\
class Section(Base):
    __tablename__="sections"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    project_id=Column(UUID(as_uuid=True),ForeignKey("projects.id",ondelete="CASCADE"))
    title=Column(String,nullable=False)
    position=Column(Integer,nullable=False)
    created_at=Column(TIMESTAMP,server_default=func.now())
class Slide(Base):
    __tablename__="slides"
    id=Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    project_id=Column(UUID(as_uuid=True),ForeignKey("projects.id",ondelete="CASCADE"))
    title=Column(String,nullable=False)
    position=Column(Integer,nullable=False)
    created_at=Column(TIMESTAMP,server_default=func.now())
    