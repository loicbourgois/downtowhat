import asyncio
import functools
from .log import logging
import time
from functools import wraps, partial
from datetime import timedelta


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


async def parallel_v2_async(
    data,
    function_async,
    loop_check=0.1,
    tabs=0,
    verbose=True,
    concurrency=20,
    update_progress=None,
):
    start_time = time.time()
    spaces = "".join(["  " for _ in range(tabs)])
    logging.info(f"{spaces}[start] {len(data)} {function_async.__name__}()")
    queue = set()
    done = set()

    def clean(i, _):
        done.add(i)
        queue.discard(i)
        percent_done = len(done) / len(data)
        if update_progress:
            update_progress(percent_done)
        if verbose:
            duration_so_far = time.time() - start_time
            full_duration = duration_so_far / percent_done
            eta = int(full_duration - duration_so_far)
            eta = str(timedelta(seconds=eta))
            logging.info(
                f"{spaces}[ end ] {function_async.__name__}() {len(done)}/{len(data)} - ETA {eta}"
            )

    task_wrappers = []
    for i, x in enumerate(data):
        task_wrappers.append(
            {
                "input": x,
            }
        )
        task_wrapper = task_wrappers[i]
        while True:
            await asyncio.sleep(loop_check)
            if len(queue) < concurrency:
                break
        if verbose:
            logging.info(
                f"{spaces}[start] {function_async.__name__}() {i+1}/{len(data)}"
            )
        queue.add(i)
        task_wrapper["task"] = asyncio.create_task(
            function_async(task_wrapper["input"])
        )
        task_wrapper["task"].add_done_callback(functools.partial(clean, i))
    for i, task_wrapper in enumerate(task_wrappers):
        task_wrapper["output"] = await task_wrapper["task"]
        del task_wrapper["task"]
        data[i] = task_wrapper["output"]
    return data


def parallel_v2(data, function_async, **kwargs):
    if kwargs.get("limit") is not None:
        return asyncio.run(
            parallel_v2_async(data[: kwargs["limit"]], function_async, **kwargs)
        )
    return asyncio.run(parallel_v2_async(data, function_async, **kwargs))
