from enum import StrEnum


class RemotePreference(StrEnum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"
    ANY = ""


class Occupation(StrEnum):
    # ── Information Technology ───────────────────────────────────────────
    SOFTWARE_ENGINEER = "software engineer"
    SOFTWARE_DEVELOPER = "software developer"
    FRONT_END_WEB_DEVELOPER = "front-end web developer"
    JAVA_DEVELOPER = "java developer"
    SQL_DEVELOPER = "sql developer"
    WEB_DEVELOPER = "web developer"
    WEB_ADMINISTRATOR = "web administrator"
    MOBILE_APPLICATION_DEVELOPER = "mobile application developer"
    COMPUTER_PROGRAMMER = "computer programmer"
    DATA_ARCHITECT = "data architect"
    DATABASE_MANAGER = "database manager"
    BUSINESS_INTELLIGENCE_DEVELOPER = "business intelligence developer"
    INFORMATION_SECURITY_ANALYST = "information security analyst"
    IT_MANAGER = "it manager"

    # ── Product ──────────────────────────────────────────────────────────
    PRODUCT_MANAGER = "product manager"
    PRODUCT_MARKETING_MANAGER = "product marketing manager"
    TECHNICAL_PRODUCT_MANAGER = "technical product manager"

    # ── Design ───────────────────────────────────────────────────────────
    UX_DESIGNER = "ux designer"
    UI_DESIGNER = "ui designer"
    UI_DEVELOPER = "ui developer"
    GRAPHIC_DESIGNER = "graphic designer"
    ART_DIRECTOR = "art director"
    ILLUSTRATOR = "illustrator"
    MULTIMEDIA_ANIMATOR = "multimedia animator"

    # ── Digital Marketing ────────────────────────────────────────────────
    DIGITAL_MARKETING_SPECIALIST = "digital marketing specialist"
    MARKETING_MANAGER = "marketing manager"
    MARKETING_ANALYST = "marketing analyst"
    SEARCH_ENGINE_OPTIMIZATION_SPECIALIST = "search engine optimization specialist"
    SOCIAL_MEDIA_MANAGER = "social media manager"
    CONTENT_MARKETING_MANAGER = "content marketing manager"
    GROWTH_MARKETER = "growth marketer"
    PERFORMANCE_MARKETING_MANAGER = "performance marketing manager"
    PAID_MEDIA_SPECIALIST = "paid media specialist"

    # ── Technical Creative ───────────────────────────────────────────────
    WRITER = "writer"
    EDITOR = "editor"
    INSTRUCTIONAL_DESIGNER = "instructional designer"
    TECHNICAL_WRITER = "technical writer"