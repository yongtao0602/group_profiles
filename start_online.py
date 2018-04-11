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
    check_input_argument(options)
    if options.path:
        for root, dirs, files in os.walk(options.path):
            for filename in files:
                temp_file = group_portrair_from_user_list('%s/%s' % (options.path, filename), options.users.split(',')[0])
                formated_output_file = format_output_file(temp_file)
                send_mail(options.users, formated_output_file)
    elif options.file:
        temp_file = group_portrair_from_user_list('%s' % options.file, options.users.split(',')[0])
        formated_output_file = format_output_file(temp_file)
        send_mail(options.users, formated_output_file)
    else:
        hive_partition_name = generate_user_list(eval(str(options)))
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
    run(options)
