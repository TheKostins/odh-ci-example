from sqlalchemy.types import String
from .BaseModel import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

class TopicModel(BaseModel):
    __tablename__ = "topics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
