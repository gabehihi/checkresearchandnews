from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


KST = ZoneInfo("Asia/Seoul")


def get_daily_window(now: datetime | None = None) -> tuple[datetime, datetime]:
    current = now.astimezone(KST) if now else datetime.now(tz=KST)
    end = current.replace(hour=8, minute=0, second=0, microsecond=0)

    if current < end:
        end -= timedelta(days=1)

    start = end - timedelta(days=1)
    return start, end


def in_window(published_at: datetime, start: datetime, end: datetime) -> bool:
    timestamp = published_at.astimezone(KST)
    return start <= timestamp < end
