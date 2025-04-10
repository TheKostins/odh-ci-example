from model import MessageModel
from repository.ORMMessageRepository import MessageRepository
class MessageService:
    def __init__(self, message_repository: MessageRepository):
        self.__message_repository = message_repository

    def get_list_by_topic(self, topic_id: int, limit: int = 100, offset: int = 0):
        return self.__message_repository.get_list_by_topic(topic_id, limit, offset);

    def post_message(self, author_nickname: str, content: str, topic_id: int) -> MessageModel:
        message = MessageModel(author_nickname=author_nickname, content=content, topic_id=topic_id)
        message = self.__message_repository.create(message)
        return message
