from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class CheckpointEntry:
    timestamp: str
    session_id: str
    mode: str
    module: str
    step: int
    status: str
    pass_id: str
    tokens_consumed: int
    cache: str


def append_checkpoint(log_path: Path, entry: CheckpointEntry) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(entry), sort_keys=True))
        handle.write("\n")


def load_checkpoints(log_path: Path) -> list[CheckpointEntry]:
    if not log_path.exists():
        return []

    entries: list[CheckpointEntry] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        entries.append(CheckpointEntry(**payload))
    return entries


def last_completed_checkpoint(
    log_path: Path,
    *,
    session_id: str,
    module: str | None = None,
) -> CheckpointEntry | None:
    candidates: Iterable[CheckpointEntry] = (
        entry
        for entry in load_checkpoints(log_path)
        if entry.session_id == session_id and entry.status == "complete"
    )

    if module is not None:
        candidates = (entry for entry in candidates if entry.module == module)

    completed = list(candidates)
    if not completed:
        return None

    return max(completed, key=lambda entry: entry.step)