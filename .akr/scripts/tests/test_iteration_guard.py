from __future__ import annotations

import pytest

from harness.iteration_guard import IterationLimitError, IterationState, assert_iteration_progress


def test_iteration_progress_allows_gap_reduction() -> None:
    previous = IterationState(iteration_number=1, open_gap_count=4, routing_decision="continue")
    current = IterationState(iteration_number=2, open_gap_count=2, routing_decision="continue")

    assert_iteration_progress(previous, current)


def test_iteration_progress_blocks_gap_regression() -> None:
    previous = IterationState(iteration_number=1, open_gap_count=2, routing_decision="continue")
    current = IterationState(iteration_number=2, open_gap_count=3, routing_decision="continue")

    with pytest.raises(AssertionError):
        assert_iteration_progress(previous, current)


def test_iteration_progress_blocks_iteration_limit() -> None:
    previous = IterationState(iteration_number=5, open_gap_count=1, routing_decision="continue")
    current = IterationState(iteration_number=6, open_gap_count=0, routing_decision="enhancement-review-close")

    with pytest.raises(IterationLimitError):
        assert_iteration_progress(previous, current)
