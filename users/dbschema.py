from sqlmodel import SQLModel, Field
from datetime import datetime


class Chats(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str
    message: str
    sender: str
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)