# @klotho::execution_unit {
#   id = "py-cross-2"
# }

async def task_sync_2(task_id: str):
    return {'id': task_id, 'status': 200, 'message': "ok"}
