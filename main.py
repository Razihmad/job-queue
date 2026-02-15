import argparse
import logging
import time
from tasks import always_success_task, flaky_task
from in_memory_queue import JobQueue
from job import Job
from queue_worker import Worker

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description="Run the job queue worker for a given time.")
    parser.add_argument(
        "--sleep",
        type=float,
        default=10,
        help="Seconds to run between worker start and stop (default: 10)",
    )
    return parser.parse_args()


def create_jobs():
    job_queue = JobQueue()
    job_queue.enqueue(Job(flaky_task, "job-1", countdown=5))
    job_queue.enqueue(Job(flaky_task, "job-2"))
    job_queue.enqueue(Job(always_success_task, "job-3"))
    return job_queue

def start_worker(job_queue: JobQueue):
    worker = Worker(job_queue)
    logger.info("Worker started")
    worker.start()
    return worker

def stop_worker(worker: Worker):
    worker.stop(timeout=15)
    logger.info("Worker stopped")


def main():
    args = parse_args()
    sleep = args.sleep
    job_queue = create_jobs()
    worker = start_worker(job_queue)
    time.sleep(sleep)
    stop_worker(worker)
    logger.info("All jobs processed")


if __name__ == "__main__":
    main()
