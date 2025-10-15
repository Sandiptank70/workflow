from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class IntegrationType(Base):
    __tablename__ = "integration_types"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    parameters = Column(Text, nullable=False)  # JSON string of parameter definitions
    tasks = Column(Text, nullable=True)  # JSON string of available tasks with metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    integrations = relationship("Integration", back_populates="integration_type", cascade="all, delete-orphan")

class Integration(Base):
    __tablename__ = "integrations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    integration_type_id = Column(Integer, ForeignKey("integration_types.id"), nullable=False)
    credentials = Column(Text, nullable=False)  # Encrypted JSON string
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    integration_type = relationship("IntegrationType", back_populates="integrations")

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    workflow_data = Column(Text, nullable=False)  # JSON string of workflow definition
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    execution_logs = relationship("ExecutionLog", back_populates="workflow", cascade="all, delete-orphan")

class ExecutionLog(Base):
    __tablename__ = "execution_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    status = Column(String(50), nullable=False)  # pending, running, success, failed
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    execution_data = Column(Text, nullable=True)  # JSON string of execution details
    error_message = Column(Text, nullable=True)
    
    # Relationships
    workflow = relationship("Workflow", back_populates="execution_logs")