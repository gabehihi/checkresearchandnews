from datetime import datetime
from zoneinfo import ZoneInfo

from src.models.schema import Article, Event
from src.pipeline.classify import classify_sector
from src.pipeline.dedup import cluster_articles
from src.pipeline.rank import rank_events
from src.pipeline.summarize import summarize_5lines


KST = ZoneInfo("Asia/Seoul")


def make_article(source: str, title: str, body: str) -> Article:
    return Article(
        published_at=datetime(2026, 2, 11, 6, 0, tzinfo=KST),
        source=source,
        title=title,
        url=f"https://example.com/{source}",
        body=body,
    )


def test_classify_semiconductor():
    sector = classify_sector("삼성전자 HBM 확대", "SK하이닉스 투자")
    assert sector == "반도체"


def test_dedup_prioritizes_maeil_business():
    articles = [
        make_article("한국경제", "같은 제목", "본문 짧음"),
        make_article("매일경제", "같은 제목", "본문 김" * 20),
    ]
    clusters = cluster_articles(articles)
    assert len(clusters) == 1
    assert clusters[0].representative.source == "매일경제"


def test_summarize_returns_5_lines():
    article = make_article("매일경제", "제목", "하나. 둘. 셋.")
    lines = summarize_5lines(article)
    assert len(lines) == 5


def test_rank_events_source_priority():
    base = make_article("한국경제", "A", "x")
    high = make_article("매일경제", "B", "x")
    events = [
        Event(event_id="1", sector="반도체", representative=base),
        Event(event_id="2", sector="반도체", representative=high),
    ]
    ranked = rank_events(events)
    assert ranked[0].representative.source == "매일경제"
