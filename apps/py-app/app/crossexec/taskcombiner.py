# TODO: can remove the exec_unit annotation once this is fixed: https://github.com/klothoplatform/klotho-pro/issues/65

# @klotho::execution_unit {
#   id = "main"
# }
from app.crossexec.task1 import task_async_1
from app.crossexec.task2 import task_sync_2
from app.crossexec.task3 import task_sync_3


async def combine_tasks():
    return [
        await task_async_1("task-1"),
        task_sync_2("task-2"),
        task_sync_3("task-3"),
    ]
