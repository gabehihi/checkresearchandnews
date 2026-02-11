from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    run_mode: str = "live"  # live | mock
    output_dir: Path = Path("reports")
    db_path: Path = Path("data/newsletter.db")
    max_articles_per_source: int = 50

    @staticmethod
    def from_env() -> "Settings":
        mode = os.getenv("NEWSLETTER_RUN_MODE", "live").strip().lower()
        if mode not in {"live", "mock"}:
            mode = "live"

        output_dir = Path(os.getenv("NEWSLETTER_OUTPUT_DIR", "reports"))
        db_path = Path(os.getenv("NEWSLETTER_DB_PATH", "data/newsletter.db"))
        max_articles = int(os.getenv("NEWSLETTER_MAX_ARTICLES_PER_SOURCE", "50"))

        return Settings(
            run_mode=mode,
            output_dir=output_dir,
            db_path=db_path,
            max_articles_per_source=max_articles,
        )
