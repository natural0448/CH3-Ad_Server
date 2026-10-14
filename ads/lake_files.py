import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from .context_projection import make_context_document
from .exporting import read_ndjson
from .timestamps import parse_utc


def stable_json(row):
    return json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def build_history(rows):
    """검증한 고유 변경을 시각·ID 순서로 반환한다. 입력·DB를 수정하지 않는다."""
    unique = {}
    for row in rows:
        # 25일차의 필드·공개 상태·출처·change_id 검사를 그대로 재사용한다.
        make_context_document(row)
        old = unique.get(row["change_id"])
        if old is not None and stable_json(old) != stable_json(row):
            raise ValueError("same change_id has conflicting content")
        unique[row["change_id"]] = row
    return sorted(unique.values(), key=lambda row: (
        parse_utc(row["event_time"]), row["change_id"]))


def build_current(history):
    """수신자별 최대 version을 고른다. 삭제 상태도 최신 후보에 남긴다."""
    current = {}
    ordered = sorted(build_history(history), key=lambda row: (
        row["media_id"], row["subject_id"], row["version"], row["change_id"]))
    for row in ordered:
        document = make_context_document(row)
        key = document["_id"]
        candidate = {"schema_version": "player-current/v1", **document}
        old = current.get(key)
        if old is None or candidate["version"] > old["version"]:
            current[key] = candidate
        elif candidate["version"] == old["version"] and (
                candidate["deleted"] != old["deleted"] or candidate["context"] != old["context"]):
            raise ValueError("same subject/version has conflicting content")
    return [current[key] for key in sorted(current)]


def write_ndjson(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(stable_json(row) + "\n")


def build_lake_version(source_path, output_dir):
    source = Path(source_path)
    output = Path(output_dir)

    source_bytes = source.read_bytes()
    source_rows = read_ndjson(source)
    history = build_history(source_rows)
    current = build_current(history)
    # 이전 버전을 덮어쓰지 않고 새 디렉터리에 결과를 쓴다.
    # [문제 2 · 한 줄] 기존 경로를 거절하는 새 출력 폴더를 만든다.
    # 예시: folder.mkdir(parents=True, exist_ok=False)
    output.mkdir(parents=True, exist_ok=False)
    files = {}
    for name, rows in (("history", history), ("current", current)):
        # [문제 3 · 여러 줄] 결과 파일을 쓰고 파일명·행 수·실제 bytes SHA를 기록한다. (4줄)
        # 예시: saved = folder / (label + ".ndjson")
        #       save_records(saved, entries)
        #       evidence[label] = {"path": saved.name, "rows": len(entries),
        #                          "sha256": hashlib.sha256(saved.read_bytes()).hexdigest()}
        pthh = output / (name + ".ndjson")
        write_ndjson(pthh, rows)
        files[name] = {
            "path": pthh.name, "rows": len(rows),
            "sha256": hashlib.sha256(pthh.read_bytes()).hexdigest()
        }
    # [문제 4 · 한 단어] 입력 SHA를 16진수 문자열로 바꾸는 메서드다.
    manifest = {
        "schema_version": "player-lake/v1", "source_kind": "player-context-change",
        "source_path": str(source), "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "input_rows": len(source_rows), "history_rows": len(history), "current_rows": len(current),
        "source_max_event_time": history[-1]["event_time"] if history else None,
        "output_dir": str(output), "files": files,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    # manifest가 없는 디렉터리는 완성 버전으로 소비하지 않는다.
    # [문제 5 · 여러 줄] manifest JSON을 UTF-8로 마지막에 저장한다. (2줄)
    # 예시: (folder / "summary.json").write_text(
    #           json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest
