.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/scheduled_thread_pool_executor.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/scheduled_thread_pool_executor
    .. image:: https://readthedocs.org/projects/scheduled_thread_pool_executor/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://scheduled_thread_pool_executor.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/scheduled_thread_pool_executor/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/scheduled_thread_pool_executor
    .. image:: https://img.shields.io/conda/vn/conda-forge/scheduled_thread_pool_executor.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/scheduled_thread_pool_executor
    .. image:: https://pepy.tech/badge/scheduled_thread_pool_executor/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/scheduled_thread_pool_executor
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/scheduled_thread_pool_executor

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/
.. image:: https://img.shields.io/pypi/v/scheduled_thread_pool_executor.svg
    :alt: PyPI-Server
    :target: https://pypi.org/project/scheduled_thread_pool_executor/
|

==============================
Scheduled Thread Pool Executor
==============================


    Scheduled Thread Pool Executor implementation in python

Makes use of delayed queue implementation to submit tasks to the thread pool.

-----
Usage
-----

.. code-block::

    from scheduled_thread_pool_executor import ScheduledThreadPoolExecutor
    scheduled_executor = ScheduledThreadPoolExecutor(max_workers=5)
    scheduled_executor.schedule(task, 0)  # equals to schedule once, where task is a callable
    scheduled_executor.schedule_at_fixed_rate(task, 0, 5)  # schedule immediately and run periodically for every 5 secs
    scheduled_executor.schedule_at_fixed_delay(task, 5, 10)  # schedule after 5secs (initial delay) and run periodically for every 10secs


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.1.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.
