from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime


class Chats(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str
    message: str
    sender: str
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)