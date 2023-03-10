from app.crossexec.task1 import task_async as task1_async
from app.crossexec.task2 import task_sync as task2_sync
from app.crossexec.task3 import task_sync_3


async def combine_tasks():
    return [
        await task1_async("task-1"),
        task2_sync("task-2"),
        task_sync_3("task-3"),
    ]
