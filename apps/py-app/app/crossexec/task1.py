# @klotho::execution_unit {
#   id = "py-cross-1"
# }

async def task_async_1(task_id: str):
    return {'id': task_id, 'status': 200, 'message': "ok"}
