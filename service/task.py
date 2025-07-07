import sqlite3
import requests
import pymysql
import json
import threading
import os
from db.engines.sqlite import get_session
from config import CONF
from core.cluster import request
import yaml
from collections import deque, Counter
from utils.nova_client import NovaClient

openstack_url_list = CONF.DEFAULT.openstack_url
dingo_command_port = CONF.DEFAULT.dingo_command_port
BASE_DIR = os.path.realpath(__file__)
test_dir = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "testcases")
target_operations = {"create_k8s_cluster", "create_classic_cluster"}
target_create_k8s = "create_k8s_cluster"
target_create_classic = "create_classic_cluster"
target_delete_k8s_cluster = "delete_k8s_cluster"
target_delete_classic_cluster = "delete_classic_cluster"
target_scale_k8s_node = "scale_k8s_node"
target_scale_classic_node = "scale_classic_node"
target_remove_classic_node = "remove_classic_node"
target_remove_k8s_node = "remove_k8s_node"

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

    def check_task_args(self):
        matched_files = []
        no_base_file = True
        err_list = []
        data_name_list = []
        for openstack_url in openstack_url_list:
            openstack_url_dir = os.path.join(test_dir, openstack_url)
            if os.path.exists(openstack_url_dir):
                for filename in os.listdir(openstack_url_dir):
                    if filename.startswith('test_') and filename.endswith('.yaml'):
                        file_path = os.path.join(openstack_url_dir, filename)
                        matched_files.append(file_path)
                    if filename == "base_config.yaml":
                        no_base_file = False
                if no_base_file:
                    err_list.append(f"In this {openstack_url_dir}, there are no file with base_config.yaml.")
        if  matched_files:
            for file_yaml in matched_files:
                with open(file_yaml, 'r', encoding='utf-8') as f:
                    dict_test_info = yaml.safe_load(f)
                    operate_list = dict_test_info.get("operate", [])
                    data_name_list.append(dict_test_info.get("data").get("name"))
                    counter = Counter(operate_list)
                    if counter["create_k8s_cluster"] > 1 and dict_test_info.get("type") == "kubernetes":
                        err_list.append(f"In this {file_yaml}, create_k8s_cluster appears more than once in "
                                        f"the operate field.")
                    if counter["create_classic_cluster"] > 1 and dict_test_info.get("type") == "classic":
                        err_list.append(f"In this {file_yaml}, create_classic_cluster appears more than once in "
                                        f"the operate field.")
                    if counter["create_classic_cluster"] > 0 and dict_test_info.get("type") == "kubernetes":
                        err_list.append(f"In this {file_yaml}, this type is kubernetes, please use create_k8s_cluster "
                                        f"in the operate field but not create_classic_cluster")
                    if counter["create_k8s_cluster"] > 0 and dict_test_info.get("type") == "classic":
                        err_list.append(f"In this {file_yaml}, this type is classic, please use create_classic_cluster "
                                        f"in the operate field but not create_k8s_cluster")
            data_name_counter = Counter(data_name_list)
            name_list = [item for item, count in data_name_counter.items() if count > 1]
            err_list.append(f"there are some cluster_name is the same, the name is {','.join(name_list)}, please check")
            if err_list:
                return None, err_list
            else:
                return True, True
        else:
            return None, []

    def handle_task_exist(self):
        # 当fastapi服务重启了，需要获取已经存在的任务是否还有为执行完的，需要检测是否要继续执行
        # 等待这些任务是否都已经完成，完成择将数据库里面的数据更新，未完成择继续等待完成即可
        # 如果发现未开始就重新执行一遍启动任务的操作即可
        pass

    def adjust_operations_deque(self, ops, create_key, delete_key):
        dq = deque(ops)

        # 移动创建操作到左端
        if create_key in dq and dq[0] != create_key:
            dq.remove(create_key)
            dq.appendleft(create_key)

        # 移动删除操作到右端
        if delete_key in dq and dq[-1] != delete_key:
            dq.remove(delete_key)
            dq.append(delete_key)

        return list(dq)

    def handle_request(self, openstack_url, cluster, token):
        url = "http://" + openstack_url + ":" + str(dingo_command_port)
        if cluster.get("type") == "kubernetes":
            for operation in cluster.get("operate"):
                if operation == target_create_k8s:
                    method = "POST"
                    response = request(url, method, cluster.get("data"), token)
            # 先创建集群，然后存入cluster_id和name到cluster表中
            # 然后执行后面的步骤，要考虑缩容和扩容的步骤，缩容时判断下node是否还有，有才能继续缩容，否则就跳过下一步
            # 如何等待结果，因为每个步骤都是一步一步执行的，只能一个操作之后才能进入下一个操作
            pass
        elif cluster.get("type") == "classic":
            for operation in cluster.get("operate"):
                if operation == target_create_classic:
                    method = "POST"
                    response = request(url, method, cluster.get("data"), token)
        else:
            pass

    def handel_task(self, openstack_url, openstack_url_dir):
        # 1、先将10.220.56.7目录下的所有测试的yaml都整理下
        # 获取token
        base_yaml_path = os.path.join(openstack_url_dir, "base_config.yaml")
        token = NovaClient(file_yaml=base_yaml_path).load_yaml()
        matched_files = []
        create_cluster_list = []
        no_create_cluster_list = []
        for filename in os.listdir(openstack_url_dir):
            if filename.startswith('test_') and filename.endswith('.yaml'):
                file_path = os.path.join(openstack_url_dir, filename)
                matched_files.append(file_path)
        # 2、把创建集群的先存放在一个列表中，把不是创建集群的存放另外一个列表中，把一些重复的动作做一个合并，
        # 比如有2次删除集群但是只有一个创建集群，就合并为创建一个集群，删除一个集群
        for file_yaml in matched_files:
            with open(file_yaml, 'r', encoding='utf-8') as f:
                dict_test_info = yaml.safe_load(f)
                operate_list = dict_test_info.get("operate", [])
                if dict_test_info.get("type") == "kubernetes":
                    dict_test_info["operate"] = self.adjust_operations_deque(operate_list, target_create_k8s,
                                                                             target_delete_k8s_cluster)
                elif dict_test_info.get("type") == "classic":
                    dict_test_info["operate"] = self.adjust_operations_deque(operate_list, target_create_classic,
                                                                             target_delete_classic_cluster)
                else:
                    pass
                if not operate_list:
                    continue
                if target_operations & set(operate_list):
                    create_cluster_list.append(dict_test_info)
                else:
                    no_create_cluster_list.append(dict_test_info)
        # 3、一些扩容和缩容的可以合并为多次执行
        threads = []
        for cluster in create_cluster_list:
            # self.handle_request(openstack_url, create_cluster_list, token)
            thread = threading.Thread(target=self.handle_request, args=(openstack_url, cluster, token))
            thread.start()
            threads.append(thread)
        # 4、检测测试用例的结果是否已经完成，并将数据写入数据库中存储起来
        for thread in threads:
            thread.join()

    def task_start(self, task_id, openstack_url=None):
        # 1、查看配置里面需要在哪些openstack环境进行自动化测试
        dict_cluster_info = {}
        threads = []
        if not openstack_url:
            for openstack_url in openstack_url_list:
                openstack_url_dir = os.path.join(test_dir, openstack_url)
                if os.path.exists(openstack_url_dir):
                    dict_cluster_info[openstack_url] = openstack_url_dir
        else:
            openstack_url_dir = os.path.join(test_dir, openstack_url)
            dict_cluster_info[openstack_url] = openstack_url_dir
        # 2、对这些openstack环境进行检测，看看这些的环境的一些参数配置是否存在，比如image和flavor（是放在这里还是放请求前,放在请求前）
        # 3、对每个openstack对应的配置文件都检查下参数是否合法， 遍历每个openstack的目录里面的所有以test_开头的文件文件，
        # 4、对每个openstack的测试用例都一一发送api请求

        for k, v in dict_cluster_info.items():
            thread = threading.Thread(target=self.handel_task, args=(k, v))
            thread.start()
            threads.append(thread)
        # 5、如果直接返回的数据有错误那就针对性的记录到数据库中，该如何处理这个错误的呢，是算所有结果里面还是需要单独拎出来再继续测吗？
        #   是否需要根据报错的信息来决定如何具体的操作
        # 6、如果直接返回的数据都是ok的，那就说明所有的api请求都是成功的，就等待结果的完成即可
        for thread in threads:
            thread.join()