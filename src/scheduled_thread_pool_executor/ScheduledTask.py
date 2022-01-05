"""Wrapper for the task submitted to ScheduledThreadPoolExecutor class"""

import time
from typing import Callable


class ScheduledTask:
    def __init__(self, runnable: Callable, initial_delay: int, period: int, *args, time_func=time.time, **kwargs):
        super().__init__()
        self.runnable = runnable
        self.initial_delay = initial_delay
        self.period = period
        self.__time_func = time_func
        self.args = args
        self.kwargs = kwargs
        self.__is_initial = True
        self.task_time = int(self.__time_func() * 1000) + (initial_delay * 1000)

    @property
    def is_initial_run(self) -> bool:
        return self.__is_initial

    @property
    def at_fixed_delay(self) -> bool:
        return self.kwargs.get('is_fixed_delay', False)

    @property
    def at_fixed_rate(self) -> bool:
        return self.kwargs.get('is_fixed_rate', False)

    @property
    def executor_ctx(self):
        return self.kwargs['executor_ctx']  # pragma: no cover

    @property
    def exception_callback(self):
        return self.kwargs.get('on_exception_callback')

    @property
    def time_func(self):
        return self.__time_func

    def __get_next_run(self) -> int:
        if not (self.at_fixed_rate or self.at_fixed_delay):
            raise TypeError("`get_next_run` invoked in a non-repeatable task")
        return int(self.__time_func() * 1000) + self.period * 1000

    def set_next_run(self, time_taken: float = 0) -> None:
        self.__is_initial = False
        self.task_time = self.__get_next_run() - time_taken

    def __lt__(self, other) -> bool:
        if not isinstance(other, ScheduledTask):
            raise TypeError(f"{other} is not of type ScheduledTask")
        return self.task_time < other.task_time

    def __repr__(self) -> str:
        return f"""(Task: {self.runnable.__name__}, Initial Delay: {self.initial_delay} second(s), Periodic: {self.period} second(s), Next run: {time.ctime(self.task_time / 1000)})"""

    def run(self, *args, **kwargs):
        st_time = time.time_ns()
        try:
            self.runnable(*self.args, **self.kwargs)
        except Exception as e:
            if self.exception_callback:
                self.exception_callback(e, *self.args, **self.kwargs)
        finally:
            end_time = time.time_ns()
            time_taken = (end_time - st_time) / 1000000  # in milliseconds
            if self.at_fixed_rate:
                self.set_next_run(time_taken)
                next_delay = (self.period*1000 - time_taken) / 1000
                if next_delay < 0 or self.task_time <= (self.__time_func()*1000):
                    self.executor_ctx._put(self, 0)
                else:
                    self.executor_ctx._put(self, next_delay)
            elif self.at_fixed_delay:
                self.set_next_run()
                self.executor_ctx._put(self, self.period)
