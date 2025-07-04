# 数据表对应的model对象

from __future__ import annotations

from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import create_engine, func
from typing_extensions import assert_type

from db.engines.mysql import get_session
from db.models.cluster.models import Cluster

class TaskSQL:

    @classmethod
    def insert(cls, task: Taskinfo):
        session = get_session()
        with session.begin():
            session.add(task)

    @classmethod
    def update(cls, task: Taskinfo):
        session = get_session()
        with session.begin():
            session.merge(task)

    @classmethod
    def list(cls, query_params, sort_keys=None, sort_dirs="ascend"):
        # 获取session
        session = get_session()
        with session.begin():
            # 根据query_params查询数据
            query = session.query(Taskinfo)
            # 查询语句

            # 数据库查询参数
            if "task_id" in query_params and query_params["task_id"]:
                query = query.filter(Taskinfo.task_id == query_params["task_id"])
            if "cluster_id" in query_params and query_params["cluster_id"]:
                query = query.filter(Taskinfo.cluster_id == query_params["cluster_id"])
            query = query.order_by(Taskinfo.start_time.desc())
            count = query.count()
            cluster_list = query.all()
            # 返回
            return count, cluster_list