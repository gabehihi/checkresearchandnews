from datetime import datetime

from src.models.schema import Article


class BaseCollector:
    source: str = ""

    def collect(self, start: datetime, end: datetime) -> list[Article]:
        raise NotImplementedError
