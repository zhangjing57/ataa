from contextlib import asynccontextmanager
from fastapi import FastAPI
from api import api_router

PROJECT_NAME = "auto_test"

app = FastAPI(
    title=PROJECT_NAME,
    openapi_url="/v1/openapi.json",
)

@app.get("/v1", description="根url")
async def root():
    return {"message": "Welcome to the auto_test!"}

app.include_router(api_router, prefix="/v1")


# 本地启动作测试使用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=5678)
