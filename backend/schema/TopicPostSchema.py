from pydantic import BaseModel, Field

class TopicPostSchema(BaseModel):
    name: str = Field(description="Name of the topic", max_length=255)
