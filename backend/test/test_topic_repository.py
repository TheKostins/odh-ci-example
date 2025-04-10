import pytest
from sqlalchemy.orm import Session
from repository.ORMTopicRepository import TopicRepository
from model.TopicModel import TopicModel

@pytest.fixture(scope="function")
def topic_repository(session: Session):
    session.query(TopicModel).delete()  # Clear the table before each test
    session.commit()
    return TopicRepository(session)

@pytest.fixture(scope="function")
def topic(session: Session) -> TopicModel:
    return TopicModel(name="Test Topic")


def test_get_existing_topic(topic_repository: TopicRepository, session: Session, topic: TopicModel):
    # Given
    session.add(topic)
    session.commit()
    session.refresh(topic)

    # When
    result = topic_repository.get(topic.id)

    # Then
    assert result is not None
    assert result.id == topic.id
    assert result.name == topic.name

def test_get_non_existing_topic(topic_repository: TopicRepository):
    # When
    result = topic_repository.get(999)

    # Then
    assert result is None

def test_get_list(topic_repository: TopicRepository, session: Session):
    # Given
    topics = [TopicModel(name=f"Topic {i}") for i in range(5)]
    session.add_all(topics)
    session.commit()

    # When
    result = topic_repository.get_list()

    # Then
    assert len(result) == 5
    assert all(isinstance(topic, TopicModel) for topic in result)

def test_create_topic(topic_repository: TopicRepository, session: Session, topic: TopicModel):
    # When
    created_topic = topic_repository.create(topic)

    # Then
    assert created_topic.id is not None
    assert created_topic.name == topic.name

def test_search_by_name(topic_repository: TopicRepository, session: Session):
    # Given
    topics = [TopicModel(name=f"Topic {i}") for i in range(5)]
    session.add_all(topics)
    session.commit()

    # When
    result = topic_repository.search_by_name("Topic 1")

    # Then
    assert len(result) == 1
    assert result[0].name == "Topic 1"

def test_search_by_name_alike(topic_repository: TopicRepository, session: Session):
    # Given
    topics = [TopicModel(name=f"Topic {i}") for i in range(5)]
    session.add_all(topics)
    session.commit()

    # When
    result = topic_repository.search_by_name("opic")

    # Then
    assert len(result) == 5
