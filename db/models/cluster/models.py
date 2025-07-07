from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 集群对象
class Cluster(Base):
    __tablename__ = "cluster"

    id = Column(Integer, primary_key= True, nullable=False, index=True, unique=False)
    cluster_id = Column(String(length=128), nullable=False)
    openstack_url = Column(String(length=128), nullable=True)
    name = Column(String(length=128), nullable=False)
    status = Column(String(length=128), nullable=True)
    status_msg = Column(Text, nullable=True)
    operate = Column(String(length=128), nullable=True)
    master_count = Column(Integer, nullable=True)
    node_count = Column(Integer, nullable=True)
    create_time = Column(DateTime, nullable=True)
    update_time = Column(DateTime, nullable=True)
    extra = Column(Text, nullable=True)