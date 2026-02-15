# Job Queue

A simple in-memory background job processor: enqueue jobs, a worker consumes them in a background thread, and failed jobs are retried up to a configurable limit (default 3 retries). Jobs can be scheduled with a countdown (ETA).

## Features

- **In-memory queue** — Thread-safe FIFO queue (no persistence)
- **Single worker** — One background thread processes jobs
- **Retries** — Failed jobs are re-queued up to `max_retries` (default 3), then marked `FAILED`
- **ETA / countdown** — Run a job after a delay with `countdown=seconds` (worker does not block while waiting)
- **Job states** — `PENDING` → `RUNNING` → `SUCCESS` / `FAILED` / `RETRYING` → `PENDING`
- **Clean lifecycle** — `Worker.start()` / `Worker.stop(timeout=...)` with optional join timeout

## Requirements

- Python 3.7+
- No external dependencies

## Quick start

```bash
python3 main.py
```

Runs the worker for 10 seconds (default), processing three sample jobs (two flaky, one always succeeding) with logging.

**Run for a custom duration:**

```bash
python3 main.py --sleep 5    # run for 5 seconds
python3 main.py --sleep 30   # run for 30 seconds
python3 main.py --help       # show all options
```

## Project structure

```
job-queue/
├── main.py            # Entry point: CLI, create jobs, start/stop worker
├── tasks.py           # Sample tasks (flaky_task, always_success_task)
├── job.py             # Job model (func, args, retries, state, eta)
├── in_memory_queue.py # JobQueue (enqueue / dequeue)
├── queue_worker.py    # Worker thread (consumes jobs, retries, respects ETA)
├── constants.py       # JobState enum
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
queue.enqueue(Job(my_task, "later", countdown=10))  # run after 10 seconds

# ... later ...
worker.stop(timeout=10)
```

## Command-line options

| Option     | Description                                      | Default |
|-----------|---------------------------------------------------|---------|
| `--sleep` | Seconds to run between worker start and stop      | `10`    |
| `-h`      | Show help                                        | —       |

## Job API

- **`Job(func, *args, max_retries=3, countdown=0)`** — Wraps a callable and its arguments.
  - Failed runs are retried at most `max_retries` times.
  - `countdown`: delay in seconds before the job is eligible to run (ETA); `0` = run immediately.
- **States**: `PENDING`, `RUNNING`, `SUCCESS`, `FAILED`, `RETRYING`.

## Worker API

- **`start()`** — Starts the worker thread.
- **`stop(timeout=None)`** — Signals stop and waits for the thread. If `timeout` is set, returns `False` if the worker didn’t exit in time.

## License

MIT
