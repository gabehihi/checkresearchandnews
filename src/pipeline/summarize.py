from src.models.schema import Article


def summarize_5lines(article: Article) -> list[str]:
    base = article.body.strip() or article.title
    sentences = [chunk.strip() for chunk in base.split(".") if chunk.strip()]

    lines = []
    for sentence in sentences[:5]:
        lines.append(sentence)

    while len(lines) < 5:
        if len(lines) == 0:
            lines.append(article.title)
        else:
            lines.append(f"추가 확인 필요 포인트 {len(lines)}")

    return lines[:5]
