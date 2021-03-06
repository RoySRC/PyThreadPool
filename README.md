![](https://www.code-inspector.com/project/11708/score/svg?branch=master)
![](https://www.code-inspector.com/project/11708/status/svg?branch=master)

# PyThreadPool
A thread pool implementation in python.

# Usage Example
```python
from thread_pool import ThreadPool
import threading

# Function to be executed by the thread pool
def sum_function(*args):
	_sum_ = 0
	thread = threading.currentThread().getName()
	for arg in args:
		_sum_ += arg
	print(thread, "sum:", _sum_)

# Instantiate a thread pool with 50 worker threads
pool = ThreadPool(50)

# Add the functions to be executed by the threadpool
for _ in range(900):
    pool.add_task(sum_function, 1, 2, 3)

# This is to prevent the threads from still running in the background
pool.kill_all_threads()

```
