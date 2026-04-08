#使用python内置的logging模块来实现日志记录功能
import logging
import os
from datetime import datetime

from utils.path_tool import get_abs_path

#日志根目录
LOG_ROOT = get_abs_path("logs")
os.makedirs(LOG_ROOT, exist_ok=True)

#格式配置(回头再看日志格式化的相关知识，先把这个放在这里)
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)

def get_logger(name:str = "agent",console_level:int = logging.INFO,file_level:int = logging.DEBUG,log_file:str = None)->logging.Logger:
    """
    获取一个配置好的logger对象
    :param name: logger的名字，默认为"agent"
    :param console_level: 控制台日志级别，默认为INFO
    :param file_level: 文件日志级别，默认为DEBUG
    :param log_file: 日志文件路径，如果为None则不写入文件
    :return: 配置好的logger对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG) #设置logger的最低日志级别为DEBUG，这样所有级别的日志都会被处理
    #防止重复添加处理器导致日志重复输出
    if logger.handlers:
        return logger

    #控制台处理器
    console_handler = logging.StreamHandler()#创建一个控制台处理器，用于将日志输出到控制台
    console_handler.setLevel(console_level) #设置控制台处理器的日志级别
    console_handler.setFormatter(DEFAULT_LOG_FORMAT) #设置控制台处理器的日志格式
    logger.addHandler(console_handler) #将控制台处理器添加到logger中

    if not log_file:#如果没有指定日志文件路径，则默认使用LOG_ROOT目录下以logger名字和当前日期命名的日志文件
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%y%m%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding='utf-8') #创建一个文件处理器，用于将日志写入文件
    file_handler.setLevel(file_level) #设置文件处理器的日志级别
    file_handler.setFormatter(DEFAULT_LOG_FORMAT) #设置文件处理器的日志格式
    logger.addHandler(file_handler) #将文件处理器添加到logger中
    return logger
logger = get_logger() #创建一个默认的logger对象，名字为"agent"，控制台日志级别为INFO，文件日志级别为DEBUG，日志文件路径默认为logs目录下以logger名字和当前日期命名的日志文件

if __name__ == "__main__":
    logger.info("信息日志")
    logger.error("错误日志")
    logger.warning("警告日志")
    logger.debug("调试日志")