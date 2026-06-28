from datetime import datetime

import httpx

from domain.models.job_post import JobPost
from .base_job_posting_service import BaseJobPostingService, SearchParams, SearchResult


class TechmapJobPostingService(BaseJobPostingService):
    BASE_URL = "https://daily-international-job-postings.p.rapidapi.com/api/v2/jobs/search"
    RAPIDAPI_HOST = "daily-international-job-postings.p.rapidapi.com"

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def search(self, params: SearchParams) -> SearchResult:
        """Call the Techmap API and return unified results."""
        query_params = self._build_query(params)
        headers = {
            "x-rapidapi-key": self._api_key,
            "x-rapidapi-host": self.RAPIDAPI_HOST,
        }

        with httpx.Client() as client:
            resp = client.get(self.BASE_URL, params=query_params, headers=headers)
            resp.raise_for_status()
            body = resp.json()

        raw_jobs = body.get("result", [])
        jobs = [self._raw_to_job_post(r) for r in raw_jobs]

        total_count = int(body["totalCount"]) if "totalCount" in body else None
        page = int(body.get("page", params.page))
        page_size = int(body.get("pageSize", params.page_size))

        return SearchResult(
            jobs=jobs,
            total_count=total_count,
            page=page,
            has_more=(page * page_size) < (total_count or 0),
        )

    # ── API-specific vocabulary mappings ──
    # Each service normalises SearchParams values to what its API expects.
    _WORK_PLACE_MAP: dict[str, str] = {
        "remote": "remote",
        "hybrid": "hybrid",
        "onsite": "onsite",
        "on-site": "onsite",
    }

    def _build_query(self, params: SearchParams) -> dict[str, str]:
        """Translate SearchParams into Techmap API query parameters."""
        q: dict[str, str] = {}

        if params.keywords:
            q["title"] = ",".join(params.keywords)

        if params.company:
            q["company"] = params.company

        if params.country_code:
            q["countryCode"] = params.country_code.lower()

        if params.city:
            q["city"] = params.city

        if params.state:
            q["state"] = params.state

        if params.posted_after:
            q["dateCreatedMin"] = params.posted_after.strftime("%Y-%m-%d")

        if params.posted_before:
            q["dateCreatedMax"] = params.posted_before.strftime("%Y-%m-%d")

        if params.occupation:
            q["occupation"] = params.occupation

        if params.work_place:
            mapped = [
                self._WORK_PLACE_MAP.get(wp.lower(), wp.lower())
                for wp in params.work_place
            ]
            q["workPlace"] = ",".join(mapped)

        if params.min_salary is not None:
            q["minSalary"] = str(params.min_salary)

        q["page"] = str(params.page)

        return q

    def _raw_to_job_post(self, raw: dict) -> JobPost:
        """Map a single Techmap API response item to the unified JobPost model."""
        json_ld = raw.get("jsonLD") or {}
        geo_point = raw.get("geoPoint") or {}
        base_salary = (json_ld.get("baseSalary") or {}).get("value") or {}

        def _parse_dt(value: str | None) -> datetime | None:
            if value:
                try:
                    return datetime.fromisoformat(value.replace("Z", "+00:00"))
                except (ValueError, TypeError):
                    return None
            return None

        max_value_str: object | None = base_salary.get("maxValue")
        max_salary_val: int | None = int(max_value_str) if max_value_str else None

        return JobPost(
            # Source
            portal=(raw.get("portal") or "").lower(),
            source_url=json_ld.get("url"),
            apply_url=json_ld.get("url"),
            # Timestamps
            created_at=_parse_dt(raw.get("dateCreated")) or datetime.now(),
            expire_at=_parse_dt(raw.get("dateExpired")),
            refreshed_at=_parse_dt(raw.get("dateActive")),
            discovered_at=None,
            # Flags
            from_company=bool(raw.get("isDirect", False)),
            from_recruiter=bool(raw.get("isRecruiter", False)),
            easy_apply=False,
            # Core listing
            title=raw.get("title") or "",
            description=json_ld.get("description"),
            # Company
            company=raw.get("company") or "",
            company_domain=None,
            industry=raw.get("industry"),
            department=raw.get("department"),
            occupation=raw.get("occupation"),
            # Location
            country_code=str(raw.get("countryCode") or "").lower() or None,
            state=raw.get("state"),
            city=raw.get("city"),
            postal_code=raw.get("postCode"),
            latitude=geo_point.get("lat"),
            longitude=geo_point.get("lon"),
            # Locale
            language=raw.get("language"),
            locale=raw.get("locale"),
            timezone=raw.get("timezone"),
            timezone_offset=raw.get("timezoneOffset"),
            # Classification
            work_place=[wp.lower() for wp in (raw.get("workPlace") or [])],
            work_type=[wt.lower() for wt in (raw.get("workType") or [])],
            contract_type=[ct.lower() for ct in (raw.get("contractType") or [])],
            career_level=[cl.lower() for cl in (raw.get("careerLevel") or [])],
            skills=raw.get("skills") or [],
            # Salary
            min_salary=raw.get("minSalary"),
            max_salary=max_salary_val,
            avg_salary_usd=None,
            salary_currency=json_ld.get("salaryCurrency"),
            salary_string=None,
        )

