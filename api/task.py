from fastapi import APIRouter, BackgroundTasks
from service.task import TaskService
import time
router = APIRouter()
taskService = TaskService()

@router.get("/task/start")
async def task_start(background_tasks: BackgroundTasks):
    """获取集群的私钥内容"""
    # 先判断下所有的配置文件的参数是否合法
    # 判断token能否获取，判断image和flavor是否存在
    try:
        # 根据id查询集群
        task_id = f"task_{int(time.time())}"
        background_tasks.add_task(taskService.task_start, task_id)
        return {"status": "Task started", "task_id": task_id}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e


