"""Public local PNG choices; advertisers cannot supply arbitrary image URLs."""
from pathlib import Path

CREATIVES = (
    {"path": "/static/ads/creatives/forest-tools.png", "label": "숲 도구점", "theme": "forest"},
    {"path": "/static/ads/creatives/camp-tea.png", "label": "모닥불 찻집", "theme": "tea"},
)
CREATIVE_PATHS = frozenset(row["path"] for row in CREATIVES)


def validate_creative(value):
    if value == "":
        return ""
    if not isinstance(value, str) or value not in CREATIVE_PATHS:
        raise ValueError("준비된 숲 도구점 또는 모닥불 찻집 이미지를 선택하세요.")
    file = Path(__file__).parent / "static/ads/creatives" / value.rsplit("/", 1)[1]
    if not file.is_file() or file.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("선택한 PNG 소재 파일을 확인하세요.")
    return value
