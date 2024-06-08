from sqlalchemy import text
from sqlmodel import Field, SQLModel, Session, create_engine, select
from typing import Optional
from enum import Enum
from datetime import datetime, timedelta


class ModelChoices(str, Enum):
    # This is a helper class to create an Enum with a label
    # by defining
    # MANUAL= "MANUAL", "Manual Task"

    def __new__(cls, value, label, color=None):
        obj = str.__new__(cls)
        obj._value_ = value
        obj.label = label
        obj.color = color
        return obj

    def __str__(self):
        return self.label

    @classmethod
    def get(cls, value):
        return cls(value)

    @classmethod
    def get_label(cls, value):
        return cls.get(value).label


class TaskType(ModelChoices):
    MANUAL = "MANUAL", "Manual Task"
    RECURRING = "RECURRING", "Recurring Task"


class TaskExecutionStatus(ModelChoices):
    PENDING = "PENDING", "Pending", "#FFA500"
    RUNNING = "RUNNING", "Running", "#FF00A5"
    COMPLETED = "COMPLETED", "Completed", "#008000"
    FAILED = "FAILED", "Failed", "#FF0000"


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    call_function: str
    type: TaskType
    frequency: Optional[int] = Field(default=None)  # Frequency in minutes for RECURRING tasks

    def execute(self, session: Session):
        execution = TaskExecution(task_id=self.id, status="PENDING")
        session.add(execution)
        session.commit()
        session.execute(text("SELECT pg_notify('task_queue', :task_id)"), {"task_id": execution.id})
        return execution

    @classmethod
    def run_tasks_forever(cls, session: Session):
        while True:
            execution = session.exec(
                select(TaskExecution).where(TaskExecution.status == TaskExecutionStatus.PENDING)).first()
            if execution:
                task = session.exec(select(Task).where(Task.id == execution.task_id)).first()
                task.perform(session)
            else:
                session.commit()
                session.execute("LISTEN task_queue")


class TaskExecution(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    start_time: Optional[datetime] = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    status: TaskExecutionStatus = TaskExecutionStatus.PENDING
    result: Optional[str] = None

    def mark_completed(self, session: Session, result: str):
        self.status = TaskExecutionStatus.COMPLETED
        self.end_time = datetime.utcnow()
        self.result = result
        session.commit()

    def mark_failed(self, session: Session, error: str):
        self.status = TaskExecutionStatus.FAILED
        self.end_time = datetime.utcnow()
        self.result = error
        session.commit()

    def perform(self, session: Session):
        try:
            self.start_time = datetime.utcnow()
            self.status = TaskExecutionStatus.RUNNING
            session.commit()

            # Simulate running the actual function
            # Replace this with actual function call logic
            result = f"Executed {self.task_id} successfully"

            self.mark_completed(session, result)
        except Exception as e:
            self.mark_failed(session, str(e))
