from model.MessageModel import MessageModel

from sqlalchemy.orm import Session
from sqlalchemy import select, func

class MessageRepository:
    def __init__(self, db: Session):
        self.__db = db

    def get_list_by_topic(self, topic_id: int, limit: int = 100, offset: int = 0) -> list[MessageModel]:
        """Get list of entities"""
        return list(self.__db.execute(
            select(MessageModel)
            .filter(MessageModel.topic_id==topic_id)
            .order_by(MessageModel.time_created.desc())
            .limit(limit).offset(offset)
        ).scalars().all())

    def get_count_by_topic(self, topic_id: int) -> int:
        """Get total count of entities"""
        return self.__db.query(func.count(MessageModel.id)).filter(MessageModel.topic_id==topic_id).scalar()


    def create(self, model: MessageModel) -> MessageModel:
        """Create entity"""
        self.__db.add(model)
        self.__db.commit()
        self.__db.refresh(model)
        return model
