import pytest
from sqlalchemy.orm import Session
from repository.ORMMessageRepository import MessageRepository
from model.MessageModel import MessageModel
from model.TopicModel import TopicModel

@pytest.fixture(scope="function")
def message_repository(session: Session) -> MessageRepository:
    session.query(MessageModel).delete()  # Clear the table before each test
    session.commit()
    return MessageRepository(session)

@pytest.fixture(scope="function")
def topic(session: Session) -> TopicModel:
    topic = TopicModel(name="Test Topic")
    session.add(topic)
    session.commit()
    session.refresh(topic)
    return topic

@pytest.fixture(scope="function")
def message(topic: TopicModel) -> MessageModel:
    return MessageModel(
        author_nickname="anonymous",
        content="Test Message",
        topic_id=topic.id
    )

def test_get_list_by_topic(message_repository: MessageRepository, session: Session, topic: TopicModel):
    # Given
    messages = [MessageModel(author_nickname="anonymous",content=f"Message {i}", topic_id=topic.id) for i in range(5)]
    session.add_all(messages)
    session.commit()

    # When
    result = message_repository.get_list_by_topic(topic.id)

    # Then
    assert len(result) == 5
    assert all(isinstance(message, MessageModel) for message in result)
    assert all(message.topic_id == topic.id for message in result)

def test_get_count_by_topic(message_repository: MessageRepository, session: Session, topic: TopicModel):
    # Given
    messages = [MessageModel(author_nickname="anonymous",content=f"Message {i}", topic_id=topic.id) for i in range(5)]
    session.add_all(messages)
    session.commit()

    # When
    count = message_repository.get_count_by_topic(topic.id)

    # Then
    assert count == 5

def test_create_message(message_repository: MessageRepository, session: Session, message: MessageModel):
    # When
    created_message = message_repository.create(message)

    # Then
    assert created_message.id is not None
    assert created_message.content == message.content
    assert created_message.topic_id == message.topic_id
