from fastapi import APIRouter
from api import cluster, task
api_router = APIRouter()
api_router.include_router(cluster.router, tags=["Cluster"])
api_router.include_router(task.router, tags=["Task"])
