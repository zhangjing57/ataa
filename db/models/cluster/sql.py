# 数据表对应的model对象

from __future__ import annotations

from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy import create_engine, func
from typing_extensions import assert_type

from db.engines.mysql import get_session
from db.models.cluster.models import Cluster

from enum import Enum

# 资产排序字段字典
class ClusterSQL:

    @classmethod
    def list_cluster(cls, query_params, page=1, page_size=10, sort_keys=None, sort_dirs="ascend"):
        # 获取session
        session = get_session()
        with session.begin():
            # 根据query_params查询数据
            query = session.query(Cluster)
            # 查询语句

            # 数据库查询参数
            if "name" in query_params and query_params["name"]:
                query = query.filter(Cluster.name.like('%' + query_params["name"] + '%'))
            if "id" in query_params and query_params["id"]:
                query = query.filter(Cluster.id == query_params["id"])
            if "operate" in query_params and query_params["operate"]:
                query = query.filter(Cluster.id == query_params["operate"])
            if "openstack_url" in query_params and query_params["openstack_url"]:
                query = query.filter(Cluster.id == query_params["openstack_url"])
            if "status" in query_params and query_params["status"]:
                query = query.filter(Cluster.status.like('%' + query_params["status"] + '%'))
            # 总数
            query = query.filter(Cluster.status != "deleted")
            count = query.count()
            # 排序
            query = query.order_by(Cluster.create_time.desc())
            # 分页条件
            page_size = int(page_size)
            page_num = int(page)
            # 查询所有数据
            if page_size == -1:
                return count, query.all()
            # 页数计算
            start = (page_num - 1) * page_size
            query = query.limit(page_size).offset(start)
            cluster_list = query.all()
            # 返回
            return count, cluster_list


    @classmethod
    def create_cluster(cls, cluster):
        # Session = sessionmaker(bind=engine, expire_on_commit=False)
        # session = Session()
        session = get_session()
        with session.begin():
            session.add(cluster)
            
    @classmethod
    def update_cluster(cls, cluster):
        # Session = sessionmaker(bind=engine, expire_on_commit=False)
        # session = Session()
        session = get_session()
        with session.begin():
            session.merge(cluster)

    @classmethod
    def delete_cluster(cls, cluster):
        # Session = sessionmaker(bind=engine, expire_on_commit=False)
        # session = Session()
        session = get_session()
        with session.begin():
            session.delete(cluster)
