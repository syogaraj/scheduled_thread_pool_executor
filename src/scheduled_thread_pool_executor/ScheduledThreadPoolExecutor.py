import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Callable

from delayedqueue import DelayedQueue
from scheduled_thread_pool_executor.ScheduledTask import ScheduledTask


class ScheduledThreadPoolExecutor(ThreadPoolExecutor):
    def __init__(self, max_workers=10, name=''):
        super().__init__(max_workers=max_workers, thread_name_prefix=name)
        self._max_workers = max_workers
        self.queue = DelayedQueue()
        self.shutdown = False

    def schedule_at_fixed_rate(self, fn: Callable, initial_delay: int, period: int, *args, **kwargs) -> bool:
        if self.shutdown:
            raise RuntimeError(f"cannot schedule new task after shutdown!")
        task = ScheduledTask(fn, initial_delay, period, *args, is_fixed_rate=True, executor_ctx=self, **kwargs)
        return self._put(task, initial_delay)

    def schedule_at_fixed_delay(self, fn: Callable, initial_delay: int, period: int, *args, **kwargs) -> bool:
        if self.shutdown:
            raise RuntimeError(f"cannot schedule new task after shutdown!")
        task = ScheduledTask(fn, initial_delay, period, *args, is_fixed_delay=True, executor_ctx=self, **kwargs)
        return self._put(task, initial_delay)

    def schedule(self, fn, initial_delay, *args, **kwargs) -> bool:
        task = ScheduledTask(fn, initial_delay, 0, *args, executor_ctx=self, **kwargs)
        return self._put(task, initial_delay)

    def _put(self, task: ScheduledTask, delay: int) -> bool:
        # Don't use this explicitly. Use schedule/schedule_at_fixed_delay/schedule_at_fixed_rate. Additionally, to be
        # called by ScheduledTask only!
        if not isinstance(task, ScheduledTask):
            raise TypeError(f"Task `{task!r}` must be of type ScheduledTask")
        if delay < 0:
            raise ValueError(f"Delay `{delay}` must be a non-negative number")
        print(f" enqueuing {task} with delay of {delay}")
        return self.queue.put(task, delay)

    def __run(self):
        while not self.shutdown:
            try:
                task: ScheduledTask = self.queue.get()
                super().submit(task.run, *task.args, **task.kwargs)
            except Exception as e:
                print(e)

    def stop(self, wait_for_completion: Optional[bool] = True):
        self.shutdown = True
        super().shutdown(wait_for_completion)

    def run(self):
        t = threading.Thread(target=self.__run)
        t.setDaemon(True)
        t.start()
