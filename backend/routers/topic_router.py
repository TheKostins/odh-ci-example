from typing import Annotated
from fastapi import APIRouter
from fastapi.params import Depends

from dependencies.deps import get_message_service, get_topic_service
from schema.MessagePostSchema import MessagePostSchema
from schema.MessageSchema import MessageSchema
from schema.PageSchema import PageSchema
from schema.TopicSchema import TopicSchema
from schema.TopicPostSchema import TopicPostSchema
from service.MessageService import MessageService
from service.TopicService import TopicService
from schema.PageSchema import create_page_schema_from_page

topic_router = APIRouter()

@topic_router.get("/topics")
def get_topics(
    topic_service: Annotated[TopicService, Depends(get_topic_service)],
    limit: int = 10,
    offset: int = 0,
    name: str | None = None,
) -> PageSchema[TopicSchema] | list[TopicSchema]:
    """
    Get a paginated list of topics.
    """
    if name:
        topics = topic_service.search_by_name(name, limit)
        return [TopicSchema.from_orm(topic) for topic in topics]
    else:
        page = topic_service.get_list(limit=limit, offset=offset)
        return create_page_schema_from_page(page, TopicSchema.from_orm)


@topic_router.get("/topics/{topic_id}")
def get_topic(
    topic_service: Annotated[TopicService, Depends(get_topic_service)],
    topic_id: int,
) -> TopicSchema:
    """
    Get a specific topic by its ID.
    """
    topic = topic_service.get_topic(topic_id)
    return TopicSchema.from_orm(topic)

@topic_router.post("/topics")
def create_topic(
    topic_service: Annotated[TopicService, Depends(get_topic_service)],
    topic: TopicPostSchema,
) -> TopicSchema:
    """
    Create a new topic.
    """
    created_topic = topic_service.create_topic(topic.name)
    return TopicSchema.from_orm(created_topic)


@topic_router.get("/topics/{topic_id}/messages")
def get_messages_by_topic(
    message_service: Annotated[MessageService, Depends(get_message_service)],
    topic_id: int,
    limit: int = 100,
    offset: int = 0,
) -> PageSchema[MessageSchema]:
    """
    Get messages for a specific topic.
    """
    page = message_service.get_list_by_topic(topic_id, limit=limit, offset=offset)
    return create_page_schema_from_page(page, MessageSchema.from_orm)


@topic_router.post("/topics/{topic_id}/messages")
def post_message(
    message_service: Annotated[MessageService, Depends(get_message_service)],
    topic_id: int,
    message: MessagePostSchema,
) -> MessageSchema:
    """
    Post a new message to a specific topic.
    """
    created_message = message_service.post_message(
        author_nickname=message.author_nickname,
        content=message.content,
        topic_id=topic_id,
    )
    return MessageSchema.from_orm(created_message)
