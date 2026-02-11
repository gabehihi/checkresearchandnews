SECTOR_KEYWORDS: dict[str, tuple[str, ...]] = {
    "부동산": ("부동산", "분양", "재건축", "재개발", "전세", "매매"),
    "반도체": ("반도체", "삼성전자", "SK하이닉스", "HBM", "파운드리", "메모리"),
    "AI": ("AI", "인공지능", "생성형", "LLM", "GPU"),
    "방산": ("방산", "국방", "미사일", "전투기", "수출 계약"),
    "조선": ("조선", "수주", "LNG선", "조선소"),
    "로봇": ("로봇", "휴머노이드", "자동화"),
    "미용/의료기기": (
        "미용",
        "의료기기",
        "휴젤",
        "파마리서치",
        "클래시스",
        "엘엔씨바이오",
        "한스바이오메드",
    ),
}


def classify_sector(title: str, body: str) -> str:
    text = f"{title} {body}".lower()
    for sector, keywords in SECTOR_KEYWORDS.items():
        if any(keyword.lower() in text for keyword in keywords):
            return sector
    return "기타"
