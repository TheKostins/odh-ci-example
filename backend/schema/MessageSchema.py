import datetime
from pydantic import BaseModel, ConfigDict

class MessageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    author_nickname: str
    content: str
    time_created: datetime.datetime
