# PyThreadPool
A thread pool implementation in python

# Usage Example
```python
from ThreadPool import ThreadPool

# Function to be executed in a thread
def function():
    print("This is a function")

# Instantiate a thread pool with 50 worker threads
pool = ThreadPool(50)

# Add the functions to be executed by the threadpool
for _ in range(5):
    pool.add_task(wait_delay)

# This is to prevent the threads from still running in the background
# The threads will not be killed until the task queue is empty. 
pool.kill_all_threads()
```
