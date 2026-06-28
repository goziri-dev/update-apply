from dataclasses import dataclass

from domain.models.enums import RemotePreference
from domain.repositories.user_profile_repository import UserProfileRepository
from infra.services.job_postings.base_job_posting_service import (
    BaseJobPostingService,
    SearchParams,
    SearchResult,
)


@dataclass
class SearchFilters:
    """Which profile fields the user wants applied as search filters.

    All default to False — opt in explicitly.
    """
    location: bool = False
    occupation: bool = False
    remote: bool = False
    salary: bool = False


@dataclass
class PersonalizedSearchInput:
    user_id: str
    page: int = 1
    page_size: int = 25
    filters: SearchFilters = SearchFilters()


class PersonalizedJobSearchService:
    """Builds a SearchParams from the user's profile applying only the
    filters the user explicitly opted into."""

    def __init__(
        self,
        profile_repo: UserProfileRepository,
        posting_service: BaseJobPostingService,
    ) -> None:
        self._profile_repo = profile_repo
        self._posting_service = posting_service

    async def search(self, input: PersonalizedSearchInput) -> SearchResult:
        profile = await self._profile_repo.read(input.user_id)

        params = SearchParams(
            keywords=[profile.desired_occupation.value],
            page=input.page,
            page_size=input.page_size,
            # Only include what the user opted into
            city=profile.desired_location_city if input.filters.location else None,
            country_code=profile.desired_location_country if input.filters.location else None,
            occupation=profile.desired_occupation.value if input.filters.occupation else None,
            work_place=(
                [profile.remote_preference.value]
                if input.filters.remote
                and profile.remote_preference
                and profile.remote_preference != RemotePreference.ANY
                else None
            ),
            min_salary=profile.salary_min if input.filters.salary else None,
        )

        return self._posting_service.search(params)
