from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[M: SQLModel]:
    def __init__(self, model_class: type, db: AsyncSession) -> None:
        self._db: AsyncSession | None = None
        self._model_class = model_class
        self._instance_not_found_error = ValueError(f"No instance of {self._model_class} with id={id} found.")
        self._no_db_set_error: Exception = ConnectionError("No database session set, please call `set_db()` to set the database")

    async def create(self, model: M) -> M:
        if not self._db:
            raise self._no_db_set_error
        self._db.add(model)
        await self._db.flush()
        await self._db.refresh(model)
        return model
        
    async def read(self, id: str) -> M:
        if not self._db:
            raise self._no_db_set_error
        instance = await self._db.get(self._model_class, id)
        if not instance:
            raise self._instance_not_found_error
        return instance
        
    async def update(self, model: M) -> M:
        if not self._db:
            raise self._no_db_set_error
        model_id = getattr(model, "id", None)
        if model_id is None:
            raise ValueError("The model has id of None or is missing an 'id' attribute")
        instance = await self._db.get(self._model_class, model_id)
        if not instance:
            raise self._instance_not_found_error
        update_data = model.model_dump(exclude={"id"}, exclude_unset=True)
        for field, value in update_data.items():
            setattr(instance, field, value)
        await self._db.flush()
        await self._db.refresh(instance)
        return instance

    async def delete(self, id: str) -> dict[str, bool]:
        if not self._db:
            raise self._no_db_set_error
        instance = await self._db.get(self._model_class, id)
        if not instance:
            raise self._instance_not_found_error
        await self._db.delete(instance)
        await self._db.flush()
        return {"ok": True}

    def set_db(self, db: AsyncSession):
        self._db = db