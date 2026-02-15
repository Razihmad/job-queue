import datetime
import uuid
from typing import Any, Callable, Optional, Tuple

from constants import JobState


class Job:
    """A single background job with a callable, args, retry policy, and optional ETA."""

    def __init__(
        self,
        func: Callable[..., Any],
        *args: Any,
        max_retries: int = 3,
        countdown: int = 0,
    ):
        if max_retries < 0 or countdown < 0:
            raise ValueError("max_retries and countdown must be non-negative")
        self.id = str(uuid.uuid4())
        self.func = func
        self.args: Tuple[Any, ...] = args
        self.max_retries = max_retries
        self.retries = 0
        self.state = JobState.PENDING
        self.eta: Optional[datetime.datetime] = (
            datetime.datetime.now() + datetime.timedelta(seconds=countdown)
            if countdown > 0
            else None
        )

    def __repr__(self) -> str:
        return f"<Job id={self.id[:8]} state={self.state.value} retries={self.retries}>"
