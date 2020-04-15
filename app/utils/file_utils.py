# coding:utf-8
import os
import time
import datetime


# 获取时间作为文件名
def get_time_as_filename():
    now = time.localtime()
    return time.strftime('%Y%m%d%H%M%S', now)


# 获取文件父级目录
def get_parent_path(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError('文件不存在')
    if not os.path.isfile(file_path):
        raise FileNotFoundError('path不能是文件夹路径')
    parent_path = os.path.dirname(file_path)

    return parent_path


# 获取文件名，去掉扩展名
def get_prefix(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError('文件不存在')
    if not os.path.isfile(file_path):
        raise FileNotFoundError('path不能是文件夹路径')
    f = os.path.basename(file_path)
    ns = f.split('.')

    return ns[0]


# 获取生成的csv的名称
def get_csv_name_via_xmind(xmind_path):
    parent_path = get_parent_path(xmind_path)
    file_prefix = '%s-%s' % (get_prefix(xmind_path), get_time_as_filename())
    altered_name = '%s.csv' % file_prefix

    return os.path.join(parent_path, altered_name)


if __name__ == '__main__':
    path = r'E:\01-智慧燃气管理平台\测试202004xx\hh'
