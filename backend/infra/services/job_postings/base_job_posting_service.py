from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from domain.models.job_post import JobPost


@dataclass
class SearchParams:
    keywords: list[str] | None
    company: str | None = None
    country_code: str | None = None
    city: str | None = None
    state: str | None = None
    occupation: str | None = None
    work_place: list[str] | None = None
    min_salary: int | None = None
    posted_after: datetime | None = None
    posted_before: datetime | None = None
    page: int = 1
    page_size: int = 25


@dataclass
class SearchResult:
    jobs: list[JobPost]
    total_count: int | None = None
    page: int = 1
    has_more: bool = False


class BaseJobPostingService(ABC):
    @abstractmethod
    def search(self, params: SearchParams) -> SearchResult:
        """Fetch jobs from the API and return JobPost models"""
        ...
    
    @abstractmethod
    def _raw_to_job_post(self, raw: dict) -> JobPost:
        """Map raw API response to the unified JobPost model"""
        ...

        