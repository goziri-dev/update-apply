from dataclasses import dataclass, field

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
    filters: SearchFilters = field(default_factory=SearchFilters)


@dataclass
class PersonalizedSearchResult:
    """Augmented result that pairs the client-side filtered job set with
    the original broad API response from the job posting service.

    Attributes:
        filtered_jobs:         Jobs that match *all* active user filters.
        filtered_total_count:  Number of jobs in the filtered set.
        page:                  Current page number.
        has_more:              Whether the *broad* API response has more pages.
        broad_result:          The original SearchResult from the posting
                               service (keywords-only query), if available.
    """
    filtered_jobs: list
    filtered_total_count: int
    page: int = 1
    has_more: bool = False
    broad_result: SearchResult | None = None


class PersonalizedJobSearchService:
    """Fetches a broad result set from the job posting API (keywords only)
    then applies the user's opted-in filters in-memory — one API call
    regardless of how many filters are active."""

    def __init__(
        self,
        profile_repo: UserProfileRepository,
        posting_service: BaseJobPostingService,
    ) -> None:
        self._profile_repo = profile_repo
        self._posting_service = posting_service

    async def search(self, input: PersonalizedSearchInput) -> PersonalizedSearchResult:
        profile = await self._profile_repo.read(input.user_id)

        # ── 1. Broad search: keywords only (single API call) ──
        broad = self._posting_service.search(SearchParams(
            keywords=[profile.desired_occupation.value],
            page=input.page,
            page_size=input.page_size,
        ))

        # ── 2. Client-side filtering ──
        filtered = list(broad.jobs)

        if input.filters.location:
            city = profile.desired_location_city
            country = profile.desired_location_country
            filtered = [
                j for j in filtered
                if (not city or (j.city or "").casefold() == city.casefold())
                and (not country or (j.country_code or "").casefold() == country.casefold())
            ]

        if input.filters.occupation:
            occ = profile.desired_occupation.value
            filtered = [
                j for j in filtered
                if (j.occupation or "").casefold() == occ.casefold()
            ]

        if input.filters.remote and profile.remote_preference != RemotePreference.ANY:
            pref = profile.remote_preference.value
            filtered = [
                j for j in filtered
                if any(pref == (wp or "").casefold() for wp in j.work_place)
            ]

        if input.filters.salary and profile.salary_min is not None:
            min_sal = profile.salary_min
            filtered = [
                j for j in filtered
                if j.min_salary is not None and j.min_salary >= min_sal
            ]

        return PersonalizedSearchResult(
            filtered_jobs=filtered,
            filtered_total_count=len(filtered),
            page=input.page,
            has_more=broad.has_more,
            broad_result=broad,
        )
