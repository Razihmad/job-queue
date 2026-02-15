# Job Queue

A simple in-memory background job processor: enqueue jobs, a worker consumes them in a background thread, and failed jobs are retried up to a configurable limit (default 3 retries).

## Features

- **In-memory queue** — Thread-safe FIFO queue (no persistence)
- **Single worker** — One background thread processes jobs
- **Retries** — Failed jobs are re-queued up to `max_retries` (default 3), then marked `FAILED`
- **Job states** — `PENDING` → `RUNNING` → `SUCCESS` / `FAILED` / `RETRYING` → `PENDING`
- **Clean lifecycle** — `Worker.start()` / `Worker.stop(timeout=...)` with optional join timeout

## Requirements

- Python 3.7+
- No external dependencies

## Quick start

```bash
python3 main.py
```

You’ll see the worker process three sample jobs (two flaky, one always succeeding) with logging.

## Project structure

```
job-queue/
├── main.py           # Demo: create queue, worker, enqueue jobs, then stop
├── example.py        # Sample tasks (flaky_task, always_success_task)
├── job.py            # Job model (func, args, retries, state)
├── in_memory_queue.py # JobQueue (enqueue / dequeue)
├── queue_worker.py   # Worker thread that consumes and retries jobs
├── constants.py      # JobState enum
└── README.md
```

## Usage

```python
from in_memory_queue import JobQueue
from job import Job
from queue_worker import Worker

def my_task(name: str) -> None:
    print(f"Hello, {name}")

queue = JobQueue()
worker = Worker(queue)
worker.start()

queue.enqueue(Job(my_task, "world"))
queue.enqueue(Job(my_task, "foo", max_retries=5))

# ... later ...
worker.stop(timeout=10)
```

## Job API

- **`Job(func, *args, max_retries=3)`** — Wraps a callable and its arguments; failed runs are retried at most `max_retries` times.
- **States**: `PENDING`, `RUNNING`, `SUCCESS`, `FAILED`, `RETRYING`.

## Worker API

- **`start()`** — Starts the worker thread.
- **`stop(timeout=None)`** — Signals stop and waits for the thread. If `timeout` is set, returns `False` if the worker didn’t exit in time.

## License

MIT
