from __future__ import annotations

from pathlib import Path

from harness.checkpoint import CheckpointEntry, append_checkpoint, last_completed_checkpoint, load_checkpoints


def test_append_and_load_checkpoints(tmp_path: Path) -> None:
    log_path = tmp_path / ".akr" / "logs" / "checkpoints.jsonl"
    entry = CheckpointEntry(
        timestamp="2026-06-01T10:00:00Z",
        session_id="akr-session-1",
        mode="generate",
        module="CourseDomain",
        step=1,
        status="complete",
        pass_id="pass1",
        tokens_consumed=8400,
        cache="hit",
    )

    append_checkpoint(log_path, entry)
    loaded = load_checkpoints(log_path)

    assert loaded == [entry]


def test_last_completed_checkpoint_filters_by_session_and_module(tmp_path: Path) -> None:
    log_path = tmp_path / ".akr" / "logs" / "checkpoints.jsonl"
    append_checkpoint(
        log_path,
        CheckpointEntry(
            timestamp="2026-06-01T10:00:00Z",
            session_id="akr-session-1",
            mode="generate",
            module="CourseDomain",
            step=1,
            status="complete",
            pass_id="pass1",
            tokens_consumed=8400,
            cache="hit",
        ),
    )
    append_checkpoint(
        log_path,
        CheckpointEntry(
            timestamp="2026-06-01T10:01:00Z",
            session_id="akr-session-1",
            mode="generate",
            module="CourseDomain",
            step=2,
            status="complete",
            pass_id="pass2",
            tokens_consumed=6200,
            cache="hit",
        ),
    )
    append_checkpoint(
        log_path,
        CheckpointEntry(
            timestamp="2026-06-01T10:02:00Z",
            session_id="akr-session-2",
            mode="generate",
            module="EnrollmentDomain",
            step=1,
            status="complete",
            pass_id="pass1",
            tokens_consumed=7100,
            cache="miss",
        ),
    )

    latest = last_completed_checkpoint(log_path, session_id="akr-session-1", module="CourseDomain")

    assert latest is not None
    assert latest.step == 2
    assert latest.pass_id == "pass2"
