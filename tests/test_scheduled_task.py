import pytest

from scheduled_thread_pool_executor.ScheduledTask import ScheduledTask


def runnable_task():
    print("a task")


@pytest.fixture
def periodic_task():
    return ScheduledTask(runnable_task, initial_delay=0, period=5)


@pytest.fixture
def non_periodic_task():
    return ScheduledTask(runnable_task, initial_delay=5, period=0)


def test_schedule_task_values(periodic_task, non_periodic_task):
    assert periodic_task.initial_delay == 0
    assert periodic_task.period == 5
    assert periodic_task.is_periodic is True
    assert periodic_task.is_initial_run is True
    assert periodic_task < non_periodic_task
    assert non_periodic_task.is_periodic is False

    periodic_task.set_next_run()
    assert periodic_task.is_initial_run is False


def test_schedule_task_errs(periodic_task, non_periodic_task):
    with pytest.raises(TypeError):
        assert non_periodic_task.set_next_run()

    with pytest.raises(TypeError):
        assert non_periodic_task < 10  # someother type which is not of ScheduledTask
