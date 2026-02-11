import sqlite3
from pathlib import Path

from src.models.schema import Article


class SQLiteStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS articles (
                    url TEXT PRIMARY KEY,
                    published_at TEXT NOT NULL,
                    source TEXT NOT NULL,
                    title TEXT NOT NULL,
                    body TEXT NOT NULL,
                    language TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def save_articles(self, articles: list[Article]) -> int:
        inserted = 0
        with self._connect() as conn:
            for article in articles:
                cur = conn.execute(
                    """
                    INSERT OR IGNORE INTO articles(url, published_at, source, title, body, language)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        article.url,
                        article.published_at.isoformat(),
                        article.source,
                        article.title,
                        article.body,
                        article.language,
                    ),
                )
                if cur.rowcount == 1:
                    inserted += 1
            conn.commit()
        return inserted
