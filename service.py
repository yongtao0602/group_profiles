# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser
from yidian.data.common.date import *
from yidian.data.common.file_job import *
from mail.mail_tools import *
from core.group_portrait import *
from core.generate_user_list import *
from core.formater import *

__author__ = 'chenpei'

reload(sys)
sys.setdefaultencoding('utf8')


def check_input_argument(options):
    if not options.users:
        parser.error('Missing REQUIRED parameters users')
        # todo: more filter
        # implement by decorator


def run(options):
    #check_input_argument(options)
    if options.path:
        for root, dirs, files in os.walk(options.path):
            for filename in files:
                #以文件的全路径（options.path+filename）和name作为作为参数，生成文件！（name是后续加载到Hive时的分区条件）
                temp_file = group_portrair_from_user_list('%s/%s' % (options.path, filename), options.users.split(',')[0])
                #格式化输出的文件：使得按照自定义的写入格式生成最终的文件
                formated_output_file = format_output_file(temp_file)
                #发送邮件
                send_mail(options.users, formated_output_file)
    elif options.file:
        print('开始解析文件。。。。。。。')
        temp_file = group_portrair_from_user_list('%s' % options.file, options.users.split(',')[0])
        formated_output_file = format_output_file(temp_file)
        send_mail(options.users, formated_output_file)
    #以上，如果是文件/文件夹，直接提取信息加载到Hive中，然后再从Hive中查询出信息，然后根据生成的信息格式化数据输出最终的用户画像文件！
    else:
        #根据name和kws来生成用户画像，这里注意执行命令行脚本时候的参数提取方法：
        #instance对象类型的options->
        # （str字符串类型->dict字典类型options（实现方法为eval(str(options))）->
        #       生成list列表类型的options.items()——>
        #           使用链表推导式提取非空值
        hive_partition_name = generate_user_list(options.__dict__)
        #注意这里是"定义的"是"直接"从用户table中获取用户画像
        temp_file=get_group_portrait_from_user_table(hive_partition_name, options.kws, options.users.split(',')[0])
        formated_output_file = format_output_file(temp_file)
        send_mail(options.users, formated_output_file)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-k", "--kws", dest="kws", help="key words")
    parser.add_option("-u", "--users", dest="users", help="the prefix of mail receiver")
    parser.add_option("-p", "--province", dest="province", help="user location province")
    parser.add_option("-c", "--city", dest="city", help="user location city")
    parser.add_option("-a", "--age", dest="age", help="should be A_40_plus,A_25_29,A_30_39,A_0_24'")
    parser.add_option("-g", "--gender", dest="gender", help="should be male, female")
    parser.add_option("-P", "--path", dest="path", help="the path of multi user id files")
    parser.add_option("-f", "--file", dest="file", help="the file location of user id")

    (options, args) = parser.parse_args()
    #options参数列表，最后生成的所有参数信息，类型是instance
    run(options)
