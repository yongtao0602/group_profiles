# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser

from yidian.data.common.date import *
from yidian.data.common.file_job import *


def get_group_portrait_from_user_table(partition_name, file_name, user):
    #tempfile.mktemp，临时文件模块
    temp_file = tempfile.mktemp(dir='/tmp', prefix='%s_%s_' % (user, file_name), suffix='.txt')
    #执行hql，并把查询结果写入临时文件
    submit_hive_query_file('core/group_portrait.hql', 'temp', hivevar={
        'PARTITION': partition_name,
        'DAY': get_datestamp_by_day_ago(2),
        'USER': user
    }, local_file=temp_file)
    return temp_file


def group_portrair_from_user_list(user_id_list_path, user):
    #获取纯文件名（去掉后缀）
    file_name = user_id_list_path.split('/')[-1].split('.')[0]
    #把该文件的信息加载到Hive中
    print('已经获取文件名'+file_name)
    load_user_list_to_hive(user_id_list_path, user)
    #把Hive数据库中数据按照一定条件查询出来，生成temp文件，并返回
    return get_group_portrait_from_user_table('local', file_name,  user)


def load_user_list_to_hive(user_id_list_path, user):
    #把数据加载到以local、$name作为分区条件的分区表里
    print('把数据加载到以'+user_id_list_path+'、'+user+'作为分区条件的分区表里')
    hql = 'load data local inpath \'%s\' overwrite into table temp.dim_group_portrait_user partition (p_type = \'local\', p_user = \'%s\')' % (user_id_list_path, user)
    submit_hive_query(hql, 'temp', queue='data')


if __name__ == '__main__':
    pass
