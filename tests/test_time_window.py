from datetime import datetime
from zoneinfo import ZoneInfo

from src.pipeline.time_window import get_daily_window, in_window


KST = ZoneInfo("Asia/Seoul")


def test_get_daily_window_after_8am():
    now = datetime(2026, 2, 11, 9, 0, tzinfo=KST)
    start, end = get_daily_window(now)
    assert start == datetime(2026, 2, 10, 8, 0, tzinfo=KST)
    assert end == datetime(2026, 2, 11, 8, 0, tzinfo=KST)


def test_get_daily_window_before_8am():
    now = datetime(2026, 2, 11, 7, 0, tzinfo=KST)
    start, end = get_daily_window(now)
    assert start == datetime(2026, 2, 9, 8, 0, tzinfo=KST)
    assert end == datetime(2026, 2, 10, 8, 0, tzinfo=KST)


def test_in_window_boundary():
    start = datetime(2026, 2, 10, 8, 0, tzinfo=KST)
    end = datetime(2026, 2, 11, 8, 0, tzinfo=KST)
    assert in_window(datetime(2026, 2, 10, 8, 0, tzinfo=KST), start, end)
    assert not in_window(datetime(2026, 2, 11, 8, 0, tzinfo=KST), start, end)
