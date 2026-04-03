import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from models import Meeting, Task, Risk, NextStep, Decision

logger = logging.getLogger(__name__)

# ==========================================
# STRATEGIC MEETING CRUD
# ==========================================
def create_full_meeting_record(db: Session, title: str, raw_text: str, intelligence: dict) -> Optional[Meeting]:
    """Atomically inserts a Meeting record with all its Decision Intelligence entities."""
    try:
        # Create core meeting with strategic metrics
        db_meeting = Meeting(
            title=title if title else "Untitled Session",
            raw_text=raw_text,
            short_summary=intelligence.get("short_summary", "Not provided."),
            detailed_summary=intelligence.get("detailed_summary", "Not provided."),
            executive_summary=intelligence.get("executive_summary", "Not provided."),
            overall_sentiment=intelligence.get("overall_sentiment", "Neutral"),
            strategic_score=intelligence.get("strategic_score", 50)
        )
        db.add(db_meeting)
        db.commit()
        db.refresh(db_meeting)
        
        # 1. Attach Decisions (New Matrix)
        for d_data in intelligence.get("decisions", []):
            db.add(Decision(
                meeting_id=db_meeting.id,
                decision_text=d_data.get('decision', 'Mandate unstated'),
                owner=d_data.get('owner', 'Management'),
                status='Active',
                confidence_score=d_data.get('confidence_score', 100),
                is_ambiguous=1 if d_data.get('is_ambiguous') else 0,
                ambiguity_reason=d_data.get('ambiguity_reason', ''),
                impact_level=d_data.get('impact_level', 'Medium')
            ))

        # 2. Attach Tasks with Predictive Analytics
        for t_data in intelligence.get("tasks", []):
            db.add(Task(
                meeting_id=db_meeting.id,
                task_description=t_data.get('task', 'Unspecified Task'),
                assigned_to=t_data.get('assigned_to', 'Unassigned'),
                deadline=t_data.get('deadline', 'Open'),
                priority=t_data.get('priority', 'Medium'),
                status='Pending',
                failure_probability=t_data.get('failure_probability', 10),
                bottleneck_detected=1 if t_data.get('bottleneck_detected') else 0
            ))
            
        # 3. Attach Strategic Risks
        for r_data in intelligence.get("risks", []):
            # Support both old string format and new dict format
            if isinstance(r_data, dict):
                db.add(Risk(
                    meeting_id=db_meeting.id, 
                    risk_text=r_data.get('risk', 'Undefined Risk'),
                    risk_level=r_data.get('risk_level', 'Moderate'),
                    prevention_strategy=r_data.get('prevention_strategy', '')
                ))
            else:
                db.add(Risk(meeting_id=db_meeting.id, risk_text=str(r_data)))
            
        # 4. Attach Next Steps
        for s_text in intelligence.get("next_steps", []):
            db.add(NextStep(meeting_id=db_meeting.id, step_text=str(s_text)))
            
        # Final Commit
        db.commit()
        return db_meeting
        
    except Exception as e:
        db.rollback()
        logger.error(f"Strategic record creation failed: {e}")
        return None

def get_recent_meetings(db: Session, limit: int = 10) -> List[Meeting]:
    """Retrieves recent meetings descending."""
    return db.query(Meeting).order_by(Meeting.created_at.desc()).limit(limit).all()

# ==========================================
# DECISION INTELLIGENCE CRUD
# ==========================================
def get_all_decisions(db: Session) -> List[Decision]:
    """Retrieves all strategic decisions across the company brain."""
    return db.query(Decision).order_by(Decision.created_at.desc()).all()

# ==========================================
# TASK & PREDICTIVE CRUD
# ==========================================
def get_all_tasks(db: Session) -> List[Task]:
    """Retrieves all tasks descending."""
    return db.query(Task).order_by(Task.created_at.desc()).all()

def update_task_status(db: Session, task_id: int, new_status: str) -> bool:
    """Updates the status of a specific task."""
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            task.status = new_status
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Task status update failed: {e}")
        return False

def remove_task(db: Session, task_id: int) -> bool:
    """Hard deletes a task from the system."""
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task:
            db.delete(task)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        logger.error(f"Task deletion failed: {e}")
        return False

# ==========================================
# RISK ANALYTICS CRUD
# ==========================================
def get_all_risks(db: Session) -> List[Risk]:
    """Retrieves all globally identified risks."""
    return db.query(Risk).order_by(Risk.created_at.desc()).all()
