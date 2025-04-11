from pydantic import BaseModel, Field

class MessagePostSchema(BaseModel):
    author_nickname: str = Field(description="Nickname of the author", max_length=100)
    content: str = Field(description="Content of the message", max_length=1000)
