from __future__ import annotations

from dataclasses import dataclass


VALID_ROUTING_DECISIONS = frozenset({
    "enhancement-review-close",
    "enhancement-test-generation",
    "continue",
})
MAX_ITERATIONS = 5


class IterationLimitError(RuntimeError):
    pass


@dataclass(frozen=True)
class IterationState:
    iteration_number: int
    open_gap_count: int
    routing_decision: str


def assert_iteration_progress(
    previous_state: IterationState,
    next_state: IterationState,
    *,
    max_iterations: int = MAX_ITERATIONS,
) -> None:
    if next_state.routing_decision not in VALID_ROUTING_DECISIONS:
        raise ValueError(
            f"Unsupported routing decision '{next_state.routing_decision}'. "
            f"Expected one of: {', '.join(sorted(VALID_ROUTING_DECISIONS))}."
        )

    if next_state.iteration_number != previous_state.iteration_number + 1:
        raise AssertionError(
            "Iteration numbering must increase exactly by 1: "
            f"{previous_state.iteration_number} -> {next_state.iteration_number}."
        )

    if next_state.iteration_number > max_iterations:
        raise IterationLimitError(
            f"Review loop reached {next_state.iteration_number} iterations without closing. "
            "Human intervention required to avoid further credit consumption."
        )

    if next_state.open_gap_count > previous_state.open_gap_count:
        raise AssertionError(
            "Iteration regression detected: open gaps increased "
            f"{previous_state.open_gap_count} -> {next_state.open_gap_count}."
        )