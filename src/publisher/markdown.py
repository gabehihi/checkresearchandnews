from datetime import datetime

from src.models.schema import Event


def render_newsletter(events: list[Event], start: datetime, end: datetime) -> str:
    lines = [
        "# 경제 뉴스레터",
        "",
        f"- 수집 구간: {start.isoformat()} ~ {end.isoformat()}",
        "",
    ]

    grouped: dict[str, list[Event]] = {}
    for event in events:
        grouped.setdefault(event.sector, []).append(event)

    for sector, sector_events in grouped.items():
        lines.append(f"## {sector}")
        for idx, event in enumerate(sector_events, start=1):
            rep = event.representative
            lines.append(f"### {idx}. {rep.title}")
            lines.append(f"- 작성일: {rep.published_at.isoformat()}")
            lines.append(f"- 신문사: {rep.source}")
            lines.append(f"- 링크: {rep.url}")
            lines.append("- 5줄 요약:")
            for no, summary_line in enumerate(event.summary_5lines, start=1):
                lines.append(f"  {no}) {summary_line}")
            if event.related_articles:
                links = ", ".join(article.url for article in event.related_articles)
                lines.append(f"- 관련뉴스: {links}")
            lines.append("")

    return "\n".join(lines).strip() + "\n"
