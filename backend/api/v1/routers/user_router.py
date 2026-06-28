import logging

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.user_job_profile_schema import (
    UpdateUserJobProfileRequest,
    UserJobProfileRequest,
)
from api.v1.schemas.user_schema import CreateUserRequest
from domain.models.user import User
from domain.models.user_job_profile import UserJobProfile
from domain.repositories.user_profile_repository import UserProfileRepository
from domain.repositories.user_repository import UserRepository
from infra.database.engine import get_session


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/user")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(payload: CreateUserRequest, user_repo: UserRepository = Depends(UserRepository), db: AsyncSession = Depends(get_session)):
    log_error = lambda error: logger.exception(f"Failed to create user: {error}")
    try:
        user_repo.set_db(db)
        return await user_repo.create(User(**payload.model_dump()))
    except ValueError as e:
        log_error(e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        log_error(e)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}") from e


@router.get("/{user_id}")
async def get_user(user_id: str, user_repo: UserRepository = Depends(UserRepository), db: AsyncSession = Depends(get_session)):
    log_error = lambda error: logger.exception(f"Failed to delete user: {error}")
    try:
        user_repo.set_db(db)
        return await user_repo.read(user_id)
    except ValueError as e:
        log_error(e)
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        log_error(e)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}") from e


@router.post("/{user_id}/profile", status_code=status.HTTP_201_CREATED)
async def create_user_job_profile(
    user_id: str,
    payload: UserJobProfileRequest,
    profile_repo: UserProfileRepository = Depends(UserProfileRepository),
    user_repo: UserRepository = Depends(UserRepository),
    db: AsyncSession = Depends(get_session),
):
    log_error = lambda error: logger.exception(f"Failed to create user job profile: {error}")
    try:
        profile_repo.set_db(db)
        user_repo.set_db(db)

        # Default profile name to the auth-provided name if not overridden
        if payload.first_name is None or payload.last_name is None:
            user = await user_repo.read(user_id)
            first_name = payload.first_name or user.first_name
            last_name = payload.last_name or user.last_name
        else:
            first_name = payload.first_name
            last_name = payload.last_name

        profile = UserJobProfile(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            current_occupation=payload.current_occupation,
            desired_occupation=payload.desired_occupation,
            years_of_experience=payload.years_of_experience,
            current_location_city=payload.current_location.city,
            current_location_country=payload.current_location.country,
            desired_location_city=payload.desired_location.city,
            desired_location_country=payload.desired_location.country,
            remote_preference=payload.remote_preference,
            salary_min=payload.salary_min,
            phone_number=payload.phone_number,
        )
        return await profile_repo.create(profile)
    except ValueError as e:
        log_error(e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        log_error(e)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}") from e


@router.get("/{user_id}/profile")
async def get_user_job_profile(
    user_id: str,
    profile_repo: UserProfileRepository = Depends(UserProfileRepository),
    db: AsyncSession = Depends(get_session),
):
    log_error = lambda error: logger.exception(f"Failed to get user job profile: {error}")
    try:
        profile_repo.set_db(db)
        return await profile_repo.read_by_user_id(user_id)
    except ValueError as e:
        log_error(e)
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        log_error(e)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}") from e


@router.put("/{user_id}/profile")
async def update_user_job_profile(
    user_id: str,
    payload: UpdateUserJobProfileRequest,
    profile_repo: UserProfileRepository = Depends(UserProfileRepository),
    db: AsyncSession = Depends(get_session),
):
    log_error = lambda error: logger.exception(f"Failed to update user job profile: {error}")
    try:
        profile_repo.set_db(db)
        existing = await profile_repo.read_by_user_id(user_id)
        return await profile_repo.update(existing, payload)
    except ValueError as e:
        log_error(e)
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        log_error(e)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}") from e