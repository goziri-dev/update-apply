import logging

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.user_schema import CreateUserRequest
from infra.database.engine import get_session
from domain.models.user import User
from domain.repositories.user_repository import UserRepository


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/user")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(payload: CreateUserRequest, db: AsyncSession = Depends(get_session)):
    log_error = lambda error: logger.exception(f"Failed to create user: {error}")
    try:
        user_repo = UserRepository(db)
        return await user_repo.create(User(**payload.model_dump()))
    except ValueError as e:
        log_error(e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        log_error(e)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}") from e


@router.get("/{user_id}")
async def get_user(user_id: str, db: AsyncSession = Depends(get_session)):
    log_error = lambda error: logger.exception(f"Failed to delete user: {error}")
    try:
        user_repo = UserRepository(db)
        return await user_repo.read(user_id)
    except ValueError as e:
        log_error(e)
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        log_error(e)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}") from e