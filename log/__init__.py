import logging
import os.path
from config import CONF

log_level = CONF.DEFAULT.loglevel
log_path= CONF.DEFAULT.log_path

def init_logger(service_name):
    logger = logging.getLogger(service_name)
    if logger.handlers:  # 如果已有 Handler，直接返回
        return logger
    logger.setLevel(log_level)  # 设置日志级别

    # 创建专属文件处理器
    service_name_log = os.path.join(log_path, "%s.log" % service_name)
    handler = logging.FileHandler(f"{service_name_log}", encoding="utf-8")
    handler.setLevel(log_level)

    # 统一日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger