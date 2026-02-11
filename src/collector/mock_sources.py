from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.collector.base import BaseCollector
from src.models.schema import Article


KST = ZoneInfo("Asia/Seoul")


class MockCollector(BaseCollector):
    def __init__(self, source: str) -> None:
        self.source = source

    def collect(self, start: datetime, end: datetime) -> list[Article]:
        midpoint = start + (end - start) / 2
        return [
            Article(
                published_at=midpoint,
                source=self.source,
                title="삼성전자·SK하이닉스 HBM 투자 확대",
                url=f"https://example.com/{self.source}/hbm",
                body="삼성전자와 SK하이닉스가 HBM 공급 확대를 위해 투자 계획을 재조정했다. "
                "글로벌 AI 수요 확대가 배경으로 꼽힌다. "
                "시장에서는 중기 실적 개선 가능성을 주목한다.",
                language="ko",
            ),
            Article(
                published_at=midpoint + timedelta(hours=1),
                source=self.source,
                title="조선 업계 LNG선 수주 증가",
                url=f"https://example.com/{self.source}/ship",
                body="국내 조선사들의 LNG선 수주가 증가했다. "
                "환율과 선가가 수익성 개선에 긍정적으로 작용했다. "
                "연간 수주 목표 달성 기대가 커지고 있다.",
                language="ko",
            ),
        ]


def build_default_collectors() -> list[BaseCollector]:
    return [
        MockCollector("매일경제"),
        MockCollector("서울경제"),
        MockCollector("한국경제"),
        MockCollector("조선일보"),
        MockCollector("동아일보"),
        MockCollector("중앙일보"),
        MockCollector("조선비즈"),
    ]
