"""Machine-readable lifecycle for P0-SF-v0.1 theory candidates."""

UNRESOLVED_CANDIDATE_STATUSES = frozenset(
    {
        "REGISTERED_UNTESTED",
        "PASSES_P0",
    }
)

TERMINAL_FAILURE_STATUSES = frozenset(
    {
        "FAILS_INDEPENDENT_MOTIVATION",
        "FAILS_DYNAMICAL_SPECIFICATION",
        "FAILS_STANDARD_LIMIT",
        "NO_ENDOGENOUS_ELLIPTIC_SECTOR",
        "ELLIPTIC_REPRESENTATION_ONLY",
        "FAILS_P1",
        "FAILS_STRUCTURE_SUFFICIENCY",
    }
)

TERMINAL_SUCCESS_STATUSES = frozenset({"PASSES_P1"})

TERMINAL_CANDIDATE_STATUSES = (
    TERMINAL_FAILURE_STATUSES | TERMINAL_SUCCESS_STATUSES
)

ALLOWED_CANDIDATE_STATUSES = (
    UNRESOLVED_CANDIDATE_STATUSES | TERMINAL_CANDIDATE_STATUSES
)

ALLOWED_TRANSITIONS = {
    "REGISTERED_UNTESTED": frozenset(
        {
            "FAILS_INDEPENDENT_MOTIVATION",
            "FAILS_DYNAMICAL_SPECIFICATION",
            "FAILS_STANDARD_LIMIT",
            "NO_ENDOGENOUS_ELLIPTIC_SECTOR",
            "ELLIPTIC_REPRESENTATION_ONLY",
            "PASSES_P0",
        }
    ),
    "PASSES_P0": frozenset(
        {
            "FAILS_P1",
            "FAILS_STRUCTURE_SUFFICIENCY",
            "PASSES_P1",
        }
    ),
}


def is_terminal(status: str) -> bool:
    return status in TERMINAL_CANDIDATE_STATUSES


def is_unresolved(status: str) -> bool:
    return status in UNRESOLVED_CANDIDATE_STATUSES


def can_transition(previous: str, current: str) -> bool:
    if previous == current:
        return True
    return current in ALLOWED_TRANSITIONS.get(previous, frozenset())
