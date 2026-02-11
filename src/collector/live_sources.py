from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from src.collector.base import BaseCollector
from src.models.schema import Article


SOURCE_DOMAIN_MAP: dict[str, str] = {
    "매일경제": "mk.co.kr",
    "서울경제": "sedaily.com",
    "한국경제": "hankyung.com",
    "조선일보": "chosun.com",
    "동아일보": "donga.com",
    "중앙일보": "joongang.co.kr",
    "조선비즈": "chosunbiz.com",
}


class GoogleNewsRSSCollector(BaseCollector):
    def __init__(self, source: str, domain: str, max_items: int = 50) -> None:
        self.source = source
        self.domain = domain
        self.max_items = max_items

    def collect(self, start: datetime, end: datetime) -> list[Article]:
        query = quote_plus(f"site:{self.domain}")
        url = f"https://news.google.com/rss/search?q={query}&hl=ko&gl=KR&ceid=KR:ko"

        with urlopen(url, timeout=15) as response:
            content = response.read()

        root = ET.fromstring(content)
        items = root.findall("./channel/item")

        articles: list[Article] = []
        for item in items[: self.max_items]:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            body = (item.findtext("description") or "").strip()
            pub_date = (item.findtext("pubDate") or "").strip()
            published = _parse_datetime(pub_date)
            if not published or not title or not link:
                continue

            articles.append(
                Article(
                    published_at=published,
                    source=self.source,
                    title=title,
                    url=link,
                    body=body,
                    language="ko",
                )
            )

        return articles


def _parse_datetime(raw: str) -> datetime | None:
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def build_live_collectors(max_items: int = 50) -> list[BaseCollector]:
    return [
        GoogleNewsRSSCollector(source=source, domain=domain, max_items=max_items)
        for source, domain in SOURCE_DOMAIN_MAP.items()
    ]
