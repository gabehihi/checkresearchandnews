# checkresearchandnews

경제 뉴스레터 자동화 서비스 코드입니다.

## 1) 환경 준비 (VSCode)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest
```

## 2) 실행 모드

- `live` (기본): Google News RSS 기반 실수집
- `mock`: 로컬 테스트용 샘플 데이터

환경변수:

```bash
export NEWSLETTER_RUN_MODE=live
export NEWSLETTER_OUTPUT_DIR=reports
export NEWSLETTER_DB_PATH=data/newsletter.db
export NEWSLETTER_MAX_ARTICLES_PER_SOURCE=50
```

실행:

```bash
python -m src.jobs.daily_0800
```

## 3) 테스트

```bash
pytest -q
```
