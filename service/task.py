import sqlite3
import requests
import pymysql
import json
from db.engines.sqlite import get_session


class TaskService:

    def get_task_info(self, cluster_id):
        # 使用requests来获取集群的信息，然后拼凑结果返回给前端
        pass

    def update_task_info(self):
        pass

    def delete_task_info(self):
        pass

    def create_task_info(self):
        pass

    def handle_task_exist(self):
        # 当fastapi服务重启了，需要获取已经存在的任务是否还有为执行完的，需要检测是否要继续执行
        # 等待这些任务是否都已经完成，完成择将数据库里面的数据更新，未完成择继续等待完成即可
        # 如果发现未开始就重新执行一遍启动任务的操作即可
        pass

    def task_start(self, task_id, openstack_url=None):
        # 1、查看配置里面需要在哪些openstack环境进行自动化测试
        # 2、对这些openstack环境进行检测，看看这些的环境的一些参数配置是否存在，比如image和flavor（是放在这里还是放请求前）
        # 3、对每个openstack对应的配置文件都检查下参数是否合法
        # 4、对每个openstack的测试用例都一一发送api请求
        # 5、如果直接返回的数据有错误那就针对性的记录到数据库中，该如何处理这个错误的呢，是算所有结果里面还是需要单独拎出来再继续测吗？
        #   是否需要根据报错的信息来决定如何具体的操作
        # 6、如果直接返回的数据都是ok的，那就说明所有的api请求都是成功的，就等待结果的完成即可
        pass