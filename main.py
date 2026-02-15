import logging
import time
from tasks import always_success_task, flaky_task
from in_memory_queue import JobQueue
from job import Job
from queue_worker import Worker

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

logger = logging.getLogger(__name__)

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
    job_queue = create_jobs()


    worker = start_worker(job_queue)
    time.sleep(10)  # Let jobs process
    stop_worker(worker)
    logger.info("All jobs processed")


if __name__ == "__main__":
    
    main()
