


# PyThreadPool
A thread pool implementation in python.

# Usage Example
```python
from thread_pool import ThreadPool
import time

# Function to be executed by the thread pool
def sum(*args):
	sum = 0
	thread = -1
	for i,arg in enumerate(args):
		sum += arg
		if i+1==len(args):
			thread = i
	print("Thread", thread, "sum:", sum)

# Instantiate a thread pool with 50 worker threads
pool = ThreadPool(50)

# Add the functions to be executed by the threadpool
for _ in range(5):
    pool.add_task(sum, 1, 2, 3, _)

# This is to prevent the threads from still running in the background
pool.kill_all_threads()
```
