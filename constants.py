from enum import Enum


class JobState(Enum):
    """Job lifecycle: PENDING → RUNNING → SUCCESS | (FAILED | RETRYING → PENDING)."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
