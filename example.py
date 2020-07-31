from thread_pool import ThreadPool

# Function to be executed by the thread pool
def sum_function(*args):
	_sum_ = 0
	thread = -1
	for i,arg in enumerate(args):
		_sum_ += arg
		if i+1==len(args):
			thread = i
	print("Thread", thread, "sum:", _sum_)

# Instantiate a thread pool with 50 worker threads
pool = ThreadPool(50)

# Add the functions to be executed by the threadpool
for _ in range(5):
    pool.add_task(sum_function, 1, 2, 3, _)

# This is to prevent the threads from still running in the background
pool.kill_all_threads()