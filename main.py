from fastapi import FastAPI
from contextlib import asynccontextmanager
from api import api_router
from log.logger import FastLOG
from jobs import cluster_status_syncer
from service.task import TaskService

PROJECT_NAME = "auto_test"

# 先执行下判断数据库中是否有正在执行的任务，防止由于fastapi重启导致的状态错误，需要重新同步下所有集群的状态
# 比如已经完成的更新下完成状态，失败的状态更新为失败的状态
TaskService().handle_task_exist()

app = FastAPI(
    title=PROJECT_NAME,
    openapi_url="/v1/openapi.json",
)

@app.get("/v1", description="根url")
async def root():
    return {"message": "Welcome to the auto_test!"}

app.include_router(api_router, prefix="/v1")
FastLOG.info("fastapi start ....................")

# 要有一个持续执行的获取真正的cluster的状态，它和结果是对应的，获取结果之后更新sqlite的数据库
# 待添加代码
@asynccontextmanager
async def lifespan(app: FastAPI):
    cluster_status_syncer.start()
    yield

app.router.lifespan_context = lifespan

# 本地启动作测试使用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=5678)
