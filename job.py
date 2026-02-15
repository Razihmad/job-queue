import uuid
from typing import Any, Callable, Tuple

from constants import JobState


class Job:
    """A single background job with a callable, args, and retry policy."""

    def __init__(
        self,
        func: Callable[..., Any],
        *args: Any,
        max_retries: int = 3,
    ):
        self.id = str(uuid.uuid4())
        self.func = func
        self.args: Tuple[Any, ...] = args
        self.max_retries = max_retries
        self.retries = 0
        self.state = JobState.PENDING

    def __repr__(self) -> str:
        return f"<Job id={self.id[:8]} state={self.state.value} retries={self.retries}>"
