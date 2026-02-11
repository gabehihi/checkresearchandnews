from collections import defaultdict
from dataclasses import dataclass
import re

from src.models.schema import Article


@dataclass
class Cluster:
    key: str
    representative: Article
    related: list[Article]


def _normalize_title(title: str) -> str:
    cleaned = re.sub(r"\s+", " ", title.strip().lower())
    return re.sub(r"[^0-9a-z가-힣 ]", "", cleaned)


def cluster_articles(articles: list[Article]) -> list[Cluster]:
    grouped: dict[str, list[Article]] = defaultdict(list)
    for article in articles:
        grouped[_normalize_title(article.title)].append(article)

    clusters: list[Cluster] = []
    for key, items in grouped.items():
        items.sort(key=lambda a: (_source_priority(a.source), -len(a.body)))
        representative = items[0]
        related = [article for article in items[1:]]
        clusters.append(Cluster(key=key, representative=representative, related=related))
    return clusters


def _source_priority(source: str) -> int:
    priority = {
        "매일경제": 0,
        "조선비즈": 1,
        "한국경제": 2,
        "서울경제": 3,
        "중앙일보": 4,
        "동아일보": 5,
        "조선일보": 6,
    }
    return priority.get(source, 99)
