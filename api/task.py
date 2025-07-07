from fastapi import APIRouter, BackgroundTasks
from service.task import TaskService
import time
from db.engines.sqlite import get_session
from config import CONF

openstack_url_list = CONF.DEFAULT.openstack_url

router = APIRouter()
taskService = TaskService()


@router.get("/task/start")
async def task_start(background_tasks: BackgroundTasks):
    # 先判断下所有的配置文件的参数是否合法
    # 针对每种类型的集群就只能操作对应的集群，否则不能生效，可以在这里判断下,只能有一个create集群，一个delete集群
    response = taskService.check_task_args()
    if not response[0] and not response[1]:
        return {"status": "there are no tasks in testcases"}
    if not response[0] and response[1]:
        return {"status": f"there are some errors in config, reason: {','.join(response[1])}"}
    # 判断token能否获取，判断image和flavor是否存在
    # 最好能控制在5秒之内返回
    try:
        if not openstack_url_list:
            return {"status": "openstack_url config arg is None, please set openstack_url config"}
        # 先判断下数据库中有没有正在进行的task任务
        # 如果有那就根据情况直接返回，如果是处于running的状态说明正在执行
        # 如果status为failed，就说明该任务已经失败，可以通过返回的错误信息，进行调整，然后重新执行
        # 只有出于running的状态不可以执行，其他状态都可以执行
        task_id = f"task_{int(time.time())}"
        background_tasks.add_task(taskService.task_start, task_id, openstack_url=None)
        return {"status": "Task started", "task_id": task_id}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e


@router.get("/task/start/{openstack_url}")
async def task_start(background_tasks: BackgroundTasks, openstack_url: str):
    # 先判断下所有的配置文件的参数是否合法
    # 判断token能否获取，判断image和flavor是否存在
    try:
        # 先判断下数据库中有没有该openstack_url正在进行的task任务
        # 如果有那就直接返回有任务正在进行中
        # 如果没有则创建该task任务
        task_id = f"task_{int(time.time())}"
        background_tasks.add_task(taskService.task_start, task_id, openstack_url)
        return {"status": "Task started", "task_id": task_id}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e


@router.get("/task/status")
async def task_status():
    try:
        # 先从数据库中获取正在running的任务的cluster信息
        # 然后把数据库中集群的状态信息返回，不是实时信息
        # 如果没有任务就直接返回没有任务在执行
        task_id = f"task_{int(time.time())}"
        return {"status": "Task started", "task_id": task_id}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e


@router.get("/task/status/runtime")
async def task_status_runtime(background_tasks: BackgroundTasks):
    try:
        # 先从数据库中获取正在running的任务的cluster信息
        # 然后去发api请求获取此时cluster的状态，是实时的信息
        # 如果没有任务就直接返回没有任务在执行
        cluster_info = None
        reponse = taskService.get_task_info(cluster_info)
        return reponse
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e

@router.get("/task/stop")
async def task_status():
    try:
        # 先从数据库中获取没有标记为deleted的任务
        # 根据task的状态是running还是failed或者success，来标记任务是否应该deleted
        task_id = f"task_{int(time.time())}"
        return {"status": "Task started", "task_id": task_id}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise e