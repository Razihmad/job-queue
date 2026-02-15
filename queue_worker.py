import logging
import threading
import time
import random
from typing import Optional

from constants import JobState
from in_memory_queue import JobQueue
from job import Job

logger = logging.getLogger(__name__)


class Worker:
    """Consumes jobs from a queue in a background thread with retry support."""

    def __init__(self, job_queue: JobQueue) -> None:
        self.job_queue = job_queue
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self) -> None:
        """Start the worker thread. Safe to call once."""
        logger.info("Worker started")
        self._thread.start()

    def stop(self, timeout: Optional[float] = None) -> bool:
        """
        Signal the worker to stop and wait for it to finish.
        If timeout is set, return False when the worker did not stop in time.
        """
        logger.info("Worker stopping...")
        self._stop_event.set()
        self._thread.join(timeout=timeout)
        stopped = not self._thread.is_alive()
        if stopped:
            logger.info("Worker stopped")
        else:
            logger.warning("Worker did not stop within timeout")
        return stopped

    def _run(self) -> None:
        while not self._stop_event.is_set():
            job = self.job_queue.dequeue()
            if not job:
                continue
            self._process_job(job)

    def _process_job(self, job: Job) -> None:
        try:
            job.state = JobState.RUNNING
            logger.info("Executing %s", job)

            # Simulate async execution
            time.sleep(random.uniform(0.5, 1.5))

            job.func(*job.args)

            job.state = JobState.SUCCESS
            logger.info("Completed %s", job)

        except Exception as e:
            job.retries += 1
            # Retry only if we haven't exceeded max_retries (avoids infinite retry loops)
            if job.retries <= job.max_retries:
                job.state = JobState.RETRYING
                logger.warning("Retrying %s due to error: %s", job, e)
                job.state = JobState.PENDING
                self.job_queue.enqueue(job)
            else:
                job.state = JobState.FAILED
                logger.error("Failed %s after max retries", job)
