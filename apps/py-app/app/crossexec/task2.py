# @klotho::execution_unit {
#   id = "py-cross-2"
# }

def task_sync(task_id: str):
    return {'id': task_id, 'status': 200, 'message': "ok"}
