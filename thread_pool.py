from threading import Thread
from queue import Queue
import numpy as np

class ThreadPool:
    """
    Thread pool containing a pool of worker threads that execute
    tasks from the task queue.
    """
    def __init__(self, num_threads):
        self.task_queue = Queue()
        self.workers = []
        self.worker_status = [False]*num_threads # store the status of the workers
        for worker_name in range(num_threads):
            self.workers.append(__Worker__(self.task_queue, worker_name, self.worker_status))

    def add_task(self, func, *args, **kargs):
        """
        Add a task to the queue. Tasks are functions that are e
        xecuted by the worker threads. Arguments to the function
        can be passed in as additional arguments to add_task
        function including keyword arguments.
        """
        self.task_queue.put((func, args, kargs))

    def wait_completion(self):
        """
        Wait for the completion of all the tasks in the queue.
        This is a blocking call that will block the calling thread
        till all the tasks in the queue is done.
        """
        self.task_queue.join()
    
    def __kill__(self):
        """ 
        Kill the worker thread
        """
        raise __KillWorkerException__("Kill")
    
    def kill_all_threads(self, wait=True):
        """ Kill all the threads in the pool """
        # wait for the completion of the current tasks in the pool
        if wait:
            self.wait_completion()
        # while there exists at least one worker that is alive
        while np.any(self.worker_status):
            # get all the alive workers
            alive_workers = np.argwhere(self.worker_status).flatten()
            # send a kill signal to all the alive workers
            for alive_worker in alive_workers:
                self.add_task(self.__kill__)

class __KillWorkerException__(Exception):
    """
    Exception to kill worker thread
    """
    pass

class __Worker__(Thread):
    """ 
    Thread executing tasks from a given tasks queue
    """
    def __init__(self, task_queue, name, status):
        Thread.__init__(self)
        self.task_queue = task_queue
        self.index = int(name)
        # indicate to the thread pool that this worker is alive
        self.status = status
        self.status[self.index] = True  
        self.start()
        
    def run(self):
        _run_ = True
        while _run_:
            # The following statement is a blocking call, i.e.
            # it will block the thread if the task queue is empty
            func, args, kargs = self.task_queue.get()
            try:
                func(*args, **kargs)
                
            except __KillWorkerException__ as e:
                # indicate to the thread pool that this worker is dead
                self.status[self.index] = False
                _run_ = False
                    
            except Exception as e:
                print(e)
                
            finally:
                self.task_queue.task_done()
