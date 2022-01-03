import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from delayedqueue import DelayedQueue

from scheduled_thread_pool_executor.ScheduledTask import ScheduledTask


class ScheduledThreadPoolExecutor(ThreadPoolExecutor):
    def __init__(self, max_workers=10, name=''):
        super().__init__(max_workers=max_workers, thread_name_prefix=name)
        self._max_workers = max_workers
        self.queue = DelayedQueue()
        self.workers = set()
        self.shutdown = False

    def schedule(self, fn, initial_delay, period: int, *args, **kwargs):
        if self.shutdown:
            raise RuntimeError(f"cannot schedule new task after shutdown!")
        task = ScheduledTask(fn, initial_delay, period, *args, **kwargs)
        print(f"submitting {task!r}")
        self.queue.put(task, initial_delay)

    def schedule_once(self, fn, initial_delay, *args, **kwargs):
        task = ScheduledTask(fn, initial_delay, 0, *args, **kwargs)
        return self.queue.put(task, initial_delay)

    def __run(self):
        while not self.shutdown:
            try:
                task: ScheduledTask = self.queue.get()
                super().submit(task.runnable, *task.args, **task.kwargs)
                if task.is_periodic:
                    task.set_next_run()
                    self.queue.put(task, task.period)
            except Exception as e:
                print(e)

    def stop(self, wait_for_completion: Optional[bool] = True):
        self.shutdown = True
        super().shutdown(wait_for_completion)

    def run(self):
        t = threading.Thread(target=self.__run)
        t.setDaemon(True)
        t.start()
