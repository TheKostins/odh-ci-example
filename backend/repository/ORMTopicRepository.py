from model.TopicModel import TopicModel
from sqlalchemy.orm import Session

from sqlalchemy import select

class TopicRepository:

    def __init__(self, db: Session):
        self.__db = db

    def get(self, id: int) -> TopicModel | None:
        """Get entity by id"""
        return self.__db.get(TopicModel, id)

    def get_list(self, limit: int = 100, offset: int = 0) -> list[TopicModel]:
        """Get list of entities"""
        return list((self.__db.execute(
            select(TopicModel).limit(limit).offset(offset))
        ).scalars().all())

    def create(self, model: TopicModel) -> TopicModel:
        """Create entity"""
        self.__db.add(model)
        self.__db.commit()
        self.__db.refresh(model)
        return model

    def update(self, model: TopicModel) -> TopicModel:
        """Update entity"""
        reattached = self.__db.merge(model)
        self.__db.commit()
        return reattached


    def delete(self, id: int) -> bool:
        """Delete entity"""
        topic = self.get(id)
        if topic is None:
            return False
        self.__db.delete(topic)
        self.__db.commit()
        return True
