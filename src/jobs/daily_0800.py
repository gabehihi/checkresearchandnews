from pathlib import Path

from src.collector.live_sources import build_live_collectors
from src.collector.mock_sources import build_default_collectors
from src.config import Settings
from src.models.schema import Event
from src.pipeline.classify import classify_sector
from src.pipeline.dedup import cluster_articles
from src.pipeline.rank import rank_events
from src.pipeline.summarize import summarize_5lines
from src.pipeline.time_window import get_daily_window, in_window
from src.publisher.markdown import render_newsletter
from src.storage.sqlite_store import SQLiteStore


def run(settings: Settings | None = None) -> Path:
    cfg = settings or Settings.from_env()
    start, end = get_daily_window()

    collectors = (
        build_default_collectors()
        if cfg.run_mode == "mock"
        else build_live_collectors(max_items=cfg.max_articles_per_source)
    )

    all_articles = []
    for collector in collectors:
        try:
            all_articles.extend(collector.collect(start, end))
        except Exception as exc:
            print(f"collector_failed source={collector.source} error={exc}")

    filtered_articles = [article for article in all_articles if in_window(article.published_at, start, end)]

    store = SQLiteStore(cfg.db_path)
    store.save_articles(filtered_articles)

    clusters = cluster_articles(filtered_articles)
    events: list[Event] = []

    for idx, cluster in enumerate(clusters, start=1):
        representative = cluster.representative
        sector = classify_sector(representative.title, representative.body)
        events.append(
            Event(
                event_id=f"evt_{start:%Y%m%d}_{idx:04d}",
                sector=sector,
                representative=representative,
                related_articles=cluster.related,
                summary_5lines=summarize_5lines(representative),
            )
        )

    ranked_events = rank_events(events)
    report = render_newsletter(ranked_events, start, end)
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    output_path = cfg.output_dir / f"newsletter_{end:%Y%m%d_%H%M}.md"
    output_path.write_text(report, encoding="utf-8")
    return output_path


if __name__ == "__main__":
    path = run()
    print(f"generated: {path}")
