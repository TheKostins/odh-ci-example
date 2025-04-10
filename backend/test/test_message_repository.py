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

def test_get_existing_message(message_repository: MessageRepository, session: Session, message: MessageModel):
    # Given
    session.add(message)
    session.commit()
    session.refresh(message)

    # When
    result = message_repository.get(message.id)

    # Then
    assert result is not None
    assert result.id == message.id
    assert result.content == message.content

def test_get_non_existing_message(message_repository: MessageRepository):
    # When
    result = message_repository.get(999)

    # Then
    assert result is None

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

def test_create_message(message_repository: MessageRepository, session: Session, message: MessageModel):
    # When
    created_message = message_repository.create(message)

    # Then
    assert created_message.id is not None
    assert created_message.content == message.content
    assert created_message.topic_id == message.topic_id

def test_update_message(message_repository: MessageRepository, session: Session, message: MessageModel):
    # Given
    session.add(message)
    session.commit()
    new_content = "Updated Message"
    message.content = new_content

    # When
    updated_message = message_repository.update(message)

    # Then
    assert updated_message.content == new_content

def test_delete_existing_message(message_repository: MessageRepository, session: Session, message: MessageModel):
    # Given
    session.add(message)
    session.commit()

    # When
    result = message_repository.delete(message.id)

    # Then
    assert result is True
    assert message_repository.get(message.id) is None

def test_delete_non_existing_message(message_repository: MessageRepository):
    # When
    result = message_repository.delete(999)

    # Then
    assert result is False
