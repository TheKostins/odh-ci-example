from sqlalchemy.schema import ForeignKey
from .BaseModel import BaseModel
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime, String

class MessageModel(BaseModel):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    author_nickname: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    topic_id : Mapped[int] = mapped_column(ForeignKey("topics.id"), nullable=False)
    time_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
