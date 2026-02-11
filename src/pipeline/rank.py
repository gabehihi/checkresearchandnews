from src.models.schema import Event


SOURCE_WEIGHT = {
    "매일경제": 10,
    "조선비즈": 9,
    "한국경제": 8,
    "서울경제": 7,
    "중앙일보": 6,
    "동아일보": 5,
    "조선일보": 4,
}


def rank_events(events: list[Event]) -> list[Event]:
    return sorted(
        events,
        key=lambda event: (
            SOURCE_WEIGHT.get(event.representative.source, 0),
            len(event.representative.body),
            event.representative.published_at,
        ),
        reverse=True,
    )
