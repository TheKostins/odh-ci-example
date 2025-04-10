from model import TopicModel
from repository.ORMTopicRepository import TopicRepository
from service.Errors import NotFountError

class TopicService:
    def __init__(self, topic_repository: TopicRepository):
        self.__topic_repository = topic_repository

    def create_topic(self, name: str) -> TopicModel:
        topic = TopicModel(name=name)
        topic = self.__topic_repository.create(topic)
        return topic

    def get_topic(self, id: int) -> TopicModel:
        topic = self.__topic_repository.get(id)
        if topic is None:
            raise NotFountError(f"Topic with id {id} not found")
        return topic

    def get_list(self, limit: int = 100, offset: int = 0) -> list[TopicModel]:
        return self.__topic_repository.get_list(limit, offset)

    def search_by_name(self, name: str, limit: int = 10) -> list[TopicModel]:
        return self.__topic_repository.search_by_name(name, limit)
