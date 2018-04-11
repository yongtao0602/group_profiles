# -*- coding: utf-8 -*-

import sys
from yidian.data.common.date import *
from yidian.data.common.file_job import *
from util.get_from_id_by_kws import *

reload(sys)
sys.setdefaultencoding('utf8')


def generate_user_list_with_specified_dims(options, user):
    day = get_datestamp_by_day_ago(2)
    column_key_map = {'gender': 'user_last_gender',
                      'age': 'user_last_age',
                      'province': 'user_last_lbs_province',
                      'city': 'user_last_lbs_city'}
    #如果k=gender，直接返回（(column_key_map[k], str.upper(options[k])），否侧返回options[k]；
    filter = ''.join(['and %s = \'%s\' ' % (i[0], i[1]) for i in map(lambda k: (column_key_map[k], str.upper(options[k]) if k == 'gender' else options[k]), options)])

    hql = 'insert overwrite table temp.dim_group_portrait_user partition (p_type = \'dims\', p_user = \'%s\') ' \
          'select distinct user_id from dw.dim_user_device_app ' \
          'where p_type = \'app\' and p_day = \'%s\' %s ;' % (user, day, filter)
    submit_hive_query(hql, 'dw', queue='data')


def generate_user_list_with_specified_profile(kws, user):
    day = get_datestamp_by_day_ago(2)
    #fromid_str获取方式，是通过访问网址后提取的，详细请移步下一层get_from_id_by_kws_list
    fromid_str = "\',\'".join(get_from_id_by_kws_list(kws))
    kws_str = "\',\'".join(kws.split('&&'))
    hql = 'insert overwrite table temp.dim_group_portrait_user partition (p_type = \'profile\', p_user = \'%s\')  ' \
          'select user_id ' \
          'from dw.fact_merge_user_profile where p_type = \'Client\' and p_day = \'%s\' and facet in (\'ens_fromid\', \'ens_ct\', \'ens_sct\', \'cs_keyword\') and interest in (\'%s\', \'%s\' ) ' \
          'having (count(distinct interest)+1)/2 >= %d ) group by user_id;' \
          % (user, day, fromid_str, kws_str, len(kws.split('&&')))
    submit_hive_query(hql, 'dw', queue='data')


def generate_user_list(options):
    #这里包含上一层的参数提取操作中最后一个步骤，这里是链表推导式
    options = {x: y for x, y in options.items() if options[x]}
    kws = options.pop('kws')
    user = options.pop('users').split(',')[0]
    #根据kws，user等信息将查询内容导入Hive特定分区中
    generate_user_list_with_specified_profile(kws, user)
    if options:
        #使用高级过滤条件查找相关的信息然后导入Hive特定分区？
        generate_user_list_with_specified_dims(options, user)
        #Q1:为什么这里又查询一次？
        submit_hive_query_file('core/generate_user_list.hql', 'dw', hivevar={'USER':user})
        return 'intersect'
    else:
        return 'profile'


if __name__ == '__main__':
    options = {
        'city': '北京',
        'gender': 'female',
        'age': 24,
        'kws': '美女'
    }
    generate_user_list(options)
