import pytest
from unittest.mock import MagicMock
from service.MessageService import MessageService
from model import MessageModel

@pytest.fixture
def mock_message_repository():
    return MagicMock()

@pytest.fixture
def message_service(mock_message_repository):
    return MessageService(mock_message_repository)

def test_get_list_by_topic(message_service, mock_message_repository):
    # Given
    topic_id = 1
    limit = 2
    offset = 0
    mock_messages = [
        MessageModel(author_nickname="User1", content="Message 1", topic_id=topic_id),
        MessageModel(author_nickname="User2", content="Message 2", topic_id=topic_id)
    ]
    mock_message_repository.get_list_by_topic.return_value = mock_messages

    # When
    result = message_service.get_list_by_topic(topic_id, limit, offset)

    # Then
    assert result == mock_messages
    mock_message_repository.get_list_by_topic.assert_called_once_with(topic_id, limit, offset)

def test_post_message(message_service, mock_message_repository):
    # Given
    author_nickname = "Anonymous"
    content = "Message content"
    topic_id = 1
    mock_message = MessageModel(author_nickname=author_nickname, content=content, topic_id=topic_id)
    mock_message_repository.create.return_value = mock_message

    # When
    result = message_service.post_message(author_nickname, content, topic_id)

    # Then
    assert result == mock_message
    mock_message_repository.create.assert_called_once()
    called_message = mock_message_repository.create.call_args[0][0]
    assert called_message.author_nickname == author_nickname
    assert called_message.content == content
    assert called_message.topic_id == topic_id
