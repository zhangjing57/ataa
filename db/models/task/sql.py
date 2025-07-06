# 数据表对应的model对象

from __future__ import annotations

from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import create_engine, func
from typing_extensions import assert_type

from db.engines.mysql import get_session
from db.models.task.models import Task

class TaskSQL:

    @classmethod
    def insert(cls, task: Task):
        session = get_session()
        with session.begin():
            session.add(task)

    @classmethod
    def update(cls, task: Task):
        session = get_session()
        with session.begin():
            session.merge(task)

    @classmethod
    def list(cls, query_params, sort_keys=None, sort_dirs="ascend"):
        # 获取session
        session = get_session()
        with session.begin():
            # 根据query_params查询数据
            query = session.query(Task)
            # 查询语句

            # 数据库查询参数
            if "task_id" in query_params and query_params["task_id"]:
                query = query.filter(Task.task_id == query_params["task_id"])
            if "cluster_id" in query_params and query_params["cluster_id"]:
                query = query.filter(Task.cluster_id == query_params["cluster_id"])
            query = query.order_by(Task.start_time.desc())
            count = query.count()
            cluster_list = query.all()
            # 返回
            return count, cluster_list