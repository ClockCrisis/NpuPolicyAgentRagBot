#为整个工程提供统一的绝对路径
import os

def get_project_root():
    "获取工程根目录的绝对路径"
    current_file = os.path.abspath(__file__) #获取当前文件的绝对路径
    current_dir = os.path.dirname(current_file)
    project_root = os.path.dirname(current_dir) #获取当前文件所在目录的父目录，即工程根目录

    return project_root

#相对路径转换为绝对路径
def get_abs_path(rel_path):
    "将相对路径转换为绝对路径"
    project_root = get_project_root()
    abs_path = os.path.join(project_root, rel_path)#将工程根目录与相对路径拼接，得到绝对路径
    return abs_path

if __name__ == "__main__":
    #测试函数
    print(get_project_root()) #打印工程根目录的绝对路径
    print(get_abs_path("data\dataset.csv")) #打印相对路径对应的绝对路径