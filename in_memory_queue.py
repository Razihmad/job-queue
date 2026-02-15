import queue
from typing import Optional

from job import Job


class JobQueue:
    """In-memory FIFO job queue (thread-safe)."""

    def __init__(self) -> None:
        self._queue: queue.Queue[Job] = queue.Queue()

    def enqueue(self, job: Job) -> None:
        """Add a job to the back of the queue."""
        self._queue.put(job)

    def dequeue(self, timeout: float = 0.2) -> Optional[Job]:
        """Remove and return the next job, or None if empty after timeout."""
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None
