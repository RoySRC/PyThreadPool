'''
MIT License

Copyright (c) 2020 RoySRC

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

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

    def empty_task_queue(self):
        """
        Remove all the unfinished tasks in the task queue
        """
        self.task_queue.queue.clear()

    def kill_all_threads(self):
        """ Kill all the threads in the pool """
        # wait for the completion of the current tasks in the pool
        self.wait_completion()
        # while there exists at least one worker that is alive
        while np.any(self.worker_status):
            # get all the alive workers
            alive_workers = np.argwhere(self.worker_status).flatten()
            # send a kill signal to all the alive workers
            for alive_worker in alive_workers:
                worker = self.workers[alive_worker]
                worker.die()
                self.add_task(self.__kill__)
        self.empty_task_queue()

class __KillWorkerException__(Exception):
    """
    Exception to kill worker thread
    """

class __Worker__(Thread):
    """
    Thread executing tasks from a given tasks queue
    """
    def __init__(self, task_queue, name, status):
        Thread.__init__(self)
        self._run_ = True
        self.task_queue = task_queue
        self.index = int(name)
        # indicate to the thread pool that this worker is alive
        self.status = status
        self.status[self.index] = True
        self.start()

    def die(self):
        """
        Make the current worker kill itself the instance
        it tries to get a task from the task queue
        """
        self._run_ = False

    def run(self):
        while self._run_:
            # The following statement is a blocking call, i.e.
            # it will block the thread if the task queue is empty
            func, args, kargs = self.task_queue.get()
            try:
                func(*args, **kargs)

            except __KillWorkerException__ as _exception_:
                # indicate to the thread pool that this worker is dead
                self.status[self.index] = False
                self._run_ = False

            except Exception as _exception_:
                print(_exception_)

            finally:
                self.task_queue.task_done()
