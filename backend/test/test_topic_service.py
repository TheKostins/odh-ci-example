import pytest
from unittest.mock import MagicMock
from service.TopicService import TopicService
from model import TopicModel
from service.Errors import NotFountError

@pytest.fixture
def mock_topic_repository():
    return MagicMock()

@pytest.fixture
def topic_service(mock_topic_repository):
    return TopicService(mock_topic_repository)

def test_create_topic(topic_service, mock_topic_repository):
    # Given
    mock_topic = TopicModel(name="Test Topic")
    mock_topic_repository.create.return_value = mock_topic

    # When
    result = topic_service.create_topic("Test Topic")

    # Then
    assert result == mock_topic
    mock_topic_repository.create.assert_called_once()
    assert mock_topic_repository.create.call_args[0][0].name == "Test Topic"

def test_get_topic(topic_service, mock_topic_repository):
    # Given
    mock_topic = TopicModel(name="Test Topic")
    mock_topic_repository.get.return_value = mock_topic

    # When
    result = topic_service.get_topic(1)

    # Then
    assert result == mock_topic
    mock_topic_repository.get.assert_called_once_with(1)

def test_get_topic_not_found(topic_service, mock_topic_repository):
    # Given
    mock_topic_repository.get.return_value = None

    # When
    with pytest.raises(NotFountError):
        topic_service.get_topic(1)

    # Then
    mock_topic_repository.get.assert_called_once_with(1)

def test_get_list(topic_service, mock_topic_repository):
    # Given
    mock_topics = [TopicModel(name="Test Topic 1"), TopicModel(name="Test Topic 2")]
    mock_topic_repository.get_list.return_value = mock_topics
    mock_topic_repository.get_total_count.return_value = 2

    # When
    result = topic_service.get_list(limit=2, offset=0)

    # Then
    assert result.items == mock_topics
    assert result.limit == 2
    assert result.offset == 0
    assert result.total == 2

    mock_topic_repository.get_list.assert_called_once_with(2, 0)
    mock_topic_repository.get_total_count.assert_called_once()

def test_search_by_name(topic_service, mock_topic_repository):
    # Given
    mock_topics = [TopicModel(name="Test Topic 1"), TopicModel(name="Test Topic 2")]
    mock_topic_repository.search_by_name.return_value = mock_topics

    # When
    result = topic_service.search_by_name("Test", limit=2)

    # Then
    assert result == mock_topics
    mock_topic_repository.search_by_name.assert_called_once_with("Test", 2)
