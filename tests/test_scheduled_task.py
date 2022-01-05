import pytest

from scheduled_thread_pool_executor.ScheduledTask import ScheduledTask
from scheduled_thread_pool_executor.ScheduledThreadPoolExecutor import ScheduledThreadPoolExecutor


def runnable_task():
    print("a task")


scheduled_thread_pool_executor = ScheduledThreadPoolExecutor()


@pytest.fixture
def periodic_task():
    return ScheduledTask(runnable_task, initial_delay=0, period=5, is_fixed_rate=True,
                         executor_ctx=scheduled_thread_pool_executor)


@pytest.fixture
def non_periodic_task():
    return ScheduledTask(runnable_task, initial_delay=5, period=0)


def test_schedule_task_values(periodic_task, non_periodic_task):
    assert periodic_task.initial_delay == 0
    assert periodic_task.period == 5
    assert periodic_task.is_initial_run is True
    assert periodic_task < non_periodic_task
    assert periodic_task.exception_callback is None

    periodic_task.set_next_run()
    assert periodic_task.is_initial_run is False


def test_schedule_task_errs(periodic_task, non_periodic_task):
    with pytest.raises(TypeError):
        assert non_periodic_task.set_next_run()

    with pytest.raises(TypeError):
        assert non_periodic_task < 10  # someother type which is not of ScheduledTask


def test_schedule_task_run(periodic_task):
    import time
    st_time = time.time_ns()
    periodic_task.run()
    end_time = time.time_ns()
    time_taken = (end_time - st_time) / 1000000  # in milliseconds
    assert ((int(periodic_task.time_func() * 1000) + periodic_task.period * 1000) - time_taken)//1000 == (
        periodic_task.task_time)//1000
