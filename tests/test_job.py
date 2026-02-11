from pathlib import Path

from src.config import Settings
from src.jobs.daily_0800 import run


def test_run_job_generates_report_and_db(tmp_path: Path):
    settings = Settings(
        run_mode="mock",
        output_dir=tmp_path / "reports",
        db_path=tmp_path / "data" / "newsletter.db",
        max_articles_per_source=5,
    )

    output = run(settings)
    assert output.exists()
    assert output.read_text(encoding="utf-8").startswith("# 경제 뉴스레터")
    assert settings.db_path.exists()
