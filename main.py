import logging

from in_memory_queue import JobQueue
from job import Job
from queue_worker import Worker
from tasks import always_success_task, flaky_task

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def create_jobs() -> JobQueue:
    job_queue = JobQueue()
    job_queue.enqueue(Job(flaky_task, "job-1", countdown=5))
    job_queue.enqueue(Job(flaky_task, "job-2"))
    job_queue.enqueue(Job(always_success_task, "job-3"))
    return job_queue


def start_worker(job_queue: JobQueue) -> Worker:
    worker = Worker(job_queue)
    worker.start()
    return worker


def stop_worker(worker: Worker) -> None:
    worker.stop(timeout=15)


def main() -> None:
    job_queue = create_jobs()
    worker = start_worker(job_queue)
    try:
        while job_queue.size() > 0:
            continue
    finally:
        stop_worker(worker)
        logger.info("All jobs processed")


if __name__ == "__main__":
    main()
