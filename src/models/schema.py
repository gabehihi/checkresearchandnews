from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Article:
    published_at: datetime
    source: str
    title: str
    url: str
    body: str
    language: str = "ko"


@dataclass
class Event:
    event_id: str
    sector: str
    representative: Article
    related_articles: list[Article] = field(default_factory=list)
    summary_5lines: list[str] = field(default_factory=list)
