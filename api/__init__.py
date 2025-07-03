from fastapi import APIRouter
from api import cluster
api_router = APIRouter()
api_router.include_router(cluster.router, tags=["Cluster"])
