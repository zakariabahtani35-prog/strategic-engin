import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Meeting(Base):
    __tablename__ = 'meetings'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, default="Untitled Session")
    raw_text = Column(Text, nullable=False, default="")
    
    short_summary = Column(Text, default="Not provided")
    detailed_summary = Column(Text, default="Not provided")
    executive_summary = Column(Text, default="Not provided")
    
    # Strategic Analytics
    overall_sentiment = Column(String(50), nullable=True, default="Neutral", server_default="Neutral")
    strategic_score = Column(Integer, nullable=True, default=50, server_default="50") # 0-100 system impact score
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    tasks = relationship("Task", back_populates="meeting", cascade="all, delete-orphan")
    decisions = relationship("Decision", back_populates="meeting", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="meeting", cascade="all, delete-orphan")
    next_steps = relationship("NextStep", back_populates="meeting", cascade="all, delete-orphan")

class Decision(Base):
    __tablename__ = 'decisions'
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id', ondelete="CASCADE"))
    
    decision_text = Column(Text, nullable=False)
    owner = Column(String(100), default="Management")
    status = Column(String(50), default="Active") # [Active, Stale, Conflict, Resolved]
    
    confidence_score = Column(Integer, nullable=True, default=100, server_default="100") # 0-100 (AI inferred)
    is_ambiguous = Column(Integer, nullable=True, default=0, server_default="0") # 0 or 1
    ambiguity_reason = Column(Text, nullable=True)
    
    impact_level = Column(String(50), nullable=True, default="Medium", server_default="Medium") # [Low, Medium, High, Critical]
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    meeting = relationship("Meeting", back_populates="decisions")

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id', ondelete="CASCADE"))
    
    task_description = Column(String(500), nullable=False)
    assigned_to = Column(String(100), default="Unassigned")
    deadline = Column(String(100), default="Open")
    priority = Column(String(50), default="Medium")
    status = Column(String(50), default="Pending")
    
    failure_probability = Column(Integer, nullable=True, default=10, server_default="10") # 0-100 predictive risk
    bottleneck_detected = Column(Integer, nullable=True, default=0, server_default="0") # 0 or 1
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    meeting = relationship("Meeting", back_populates="tasks")

class Risk(Base):
    __tablename__ = 'risks'
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id', ondelete="CASCADE"))
    
    risk_text = Column(Text, nullable=False)
    risk_level = Column(String(50), nullable=True, default="Moderate", server_default="Moderate") # [Low, Moderate, Critical]
    prevention_strategy = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    meeting = relationship("Meeting", back_populates="risks")

class NextStep(Base):
    __tablename__ = 'next_steps'
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey('meetings.id', ondelete="CASCADE"))
    
    step_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    meeting = relationship("Meeting", back_populates="next_steps")
