# -*- coding: utf-8 -*-

import time
import sys
import pymysql
from yidian.data.common.date import *
from yidian.data.common.file_job import *

# todo 支持在线提交任务, 以任务队列形式工作， 与前端交互
# todo 使用scala重构， 代替python + hive， graceful

def get_all_todo_job():
    conn = pymysql.connect(host=MYSQL_PARAM['host'], port=3309, user='olap', passwd='olap', db='growth')

def update_job_status(id):
    pass

if __name__ == '__main__':
    pass