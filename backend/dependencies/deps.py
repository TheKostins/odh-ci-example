from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.orm import Session

from config.database import get_session

from repository.ORMMessageRepository import MessageRepository
from repository.ORMTopicRepository import TopicRepository

from service.MessageService import MessageService
from service.TopicService import TopicService

def get_message_repository(session: Annotated[Session, Depends(get_session)]):
    return MessageRepository(session)

def get_topic_repository(session: Annotated[Session, Depends(get_session)]):
    return TopicRepository(session)

def get_message_service(
    message_repository: Annotated[MessageRepository, Depends(get_message_repository)]
):
    return MessageService(message_repository)

def get_topic_service(
    topic_repository: Annotated[TopicRepository, Depends(get_topic_repository)]
):
    return TopicService(topic_repository)
