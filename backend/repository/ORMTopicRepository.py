from model.TopicModel import TopicModel
from sqlalchemy.orm import Session

from sqlalchemy import select, func

class TopicRepository:

    def __init__(self, db: Session):
        self.__db = db

    def get(self, id: int) -> TopicModel | None:
        """Get entity by id"""
        return self.__db.get(TopicModel, id)

    def get_total_count(self) -> int:
        """Get total count of entities"""
        return self.__db.query(func.count(TopicModel.id)).scalar()

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

    def search_by_name(self, name: str, limit: int = 10) -> list[TopicModel]:
        """Search for topics by name"""
        return list(self.__db.execute(
            select(TopicModel).filter(TopicModel.name.ilike(f"%{name}%")).limit(limit)
        ).scalars().all())
