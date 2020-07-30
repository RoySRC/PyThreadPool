from ThreadPool import ThreadPool
import time

# Function to be executed in a thread
def function():
    print("This is a function")
    time.sleep(1)
    print("Function done.")
    
# Instantiate a thread pool with 50 worker threads
pool = ThreadPool(50)

# Add the functions to be executed by the threadpool
for _ in range(5):
    pool.add_task(function)

# This is to prevent the threads from still running in the background
pool.kill_all_threads()
