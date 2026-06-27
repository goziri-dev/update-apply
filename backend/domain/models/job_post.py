from datetime import datetime
from typing import Literal

from sqlmodel import SQLModel, Field


class JobPost(SQLModel, table=True):
    # Source
    portal: str
    source_url: str | None = None
    apply_url: str | None = None

    # Timestamps
    created_at: datetime
    expire_at: datetime | None = None
    refreshed_at: datetime | None = None
    discovered_at: datetime | None = None

    # Flags
    from_company: bool
    from_recruiter: bool
    easy_apply: bool = False

    # Core listing
    title: str
    description: str | None = None

    # Company
    company: str
    company_domain: str | None = None
    industry: str | None = None
    department: str | None = None
    occupation: str | None = None

    # Location
    country_code: str | None = None
    state: str | None = None
    city: str | None = None
    postal_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    # Locale
    language: str | None = None
    locale: str | None = None
    timezone: str | None = None
    timezone_offset: int | None = None

    # Classification
    work_place: list[Literal["onsite", "hybrid", "remote"]] = Field(default_factory=list)
    work_type: list[str] = Field(default_factory=list)
    contract_type: list[str] = Field(default_factory=list)
    career_level: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)

    # Salary
    min_salary: int | None = None
    max_salary: int | None = None
    avg_salary_usd: int | None = None
    salary_currency: str | None = None
    salary_string: str | None = None