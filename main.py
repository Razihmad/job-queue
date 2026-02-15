import logging
import time
from example import always_success_task, flaky_task
from in_memory_queue import JobQueue
from job import Job
from queue_worker import Worker

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

logger = logging.getLogger(__name__)


def main():
    job_queue = JobQueue()
    worker = Worker(job_queue)

    worker.start()

    job_queue.enqueue(Job(flaky_task, "job-1"))
    job_queue.enqueue(Job(flaky_task, "job-2"))
    job_queue.enqueue(Job(always_success_task, "job-3"))

    time.sleep(10)  # Let jobs process

    worker.stop(timeout=15)  # Optional: avoid blocking forever if a job hangs
    logger.info("All jobs processed")

if __name__ == "__main__":
    main()
