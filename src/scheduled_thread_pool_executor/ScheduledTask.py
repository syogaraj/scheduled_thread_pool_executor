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
    def is_periodic(self) -> bool:
        return self.period != 0

    @property
    def is_initial_run(self) -> bool:
        return self.__is_initial

    def __get_next_run(self) -> int:
        if not self.is_periodic:
            raise TypeError("`get_next_run` invoked in a non-repeatable task")
        return int(self.__time_func() * 1000) + self.period * 1000

    def set_next_run(self) -> None:
        self.__is_initial = False
        self.task_time = self.__get_next_run()

    def __lt__(self, other) -> bool:
        if not isinstance(other, ScheduledTask):
            raise TypeError(f"{other} is not of type ScheduledTask")
        return self.task_time < other.task_time

    def __repr__(self) -> str:
        return f"""(Task: {self.runnable.__name__}, Initial Delay: {self.initial_delay} second(s), Periodic: {self.is_periodic} / {self.period} second(s), Next run: {time.ctime(self.task_time / 1000)}"""
