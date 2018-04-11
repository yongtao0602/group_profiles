# -*- coding: utf-8 -*-

import time
import sys
from optparse import OptionParser
#from collections import OrderedDict
from yidian.data.common.date import *
from yidian.data.common.file_job import *

ordered_keys = ["ens_gender", "ens_age", "lbs_area", "lbs_tier", "lbs_province", "lbs_city", "os", "ens_ct", "ens_sct", "ens_fromid", "cs_keyword"]

def format_output_file(input_file):
    format_map = {
        "ens_gender": {'name': '性别',
                       'max': 0,
                       'format_script': 'cat %s | grep ens_gender | awk \'{print $2, $4}\' | sort -n -r -k 2 >> %s'},
        "ens_age": {'name': '年龄',
                    'max': 0,
                    'format_script': 'cat %s | grep ens_age | awk \'{print $2, $4}\' | sort -n -r -k 2  >> %s'},
        "lbs_area": {'name': '地域',
                     'max': 0,
                     'format_script': 'cat %s | grep lbs_area | awk \'$3>1 {print $2, $3}\' | sort -n -r -k 2  >> %s'},
        "lbs_tier": {'name': '几线城市',
                     'max': 0,
                     'format_script': 'cat %s | grep lbs_tier | awk \'{print $2, $3}\' | sort -n -r -k 2 >> %s'},
        "lbs_province": {'name': '省份',
                         'max': 0,
                         'format_script': 'cat %s | grep lbs_province | sort -n -k 3 -r  | awk \'$4>1 {print $2, $3}\' | head -50 >> %s '},
        "lbs_city": {'name': '城市',
                     'max': 0,
                     'format_script': 'cat %s | grep lbs_city | sort -n -k 3 -r  | head -100 | awk \'{print $2, $3}\' | head -80>> %s'},
        "ens_ct": {'name': '大类',
                   'max': 0,
                   'format_script': 'cat %s | grep ens_ct | sort -n -r -k 3 | awk -v max=%s \'{print $2, $3/max}\' | head -100 | tr \'\n\' \',\' | tr \' \' \':\'>> %s'},
        "ens_sct": {'name': '小类',
                    'max': 0,
                    'format_script': 'cat %s | grep ens_sct |sort -n -r -k 3 | awk -v max=%s \'{print $2, $3/max}\' | head -100 | tr \'\n\' \',\' | tr \' \' \':\'>> %s'},
        "ens_fromid": {'name': '频道',
                       'max': 0,
                       'format_script': 'cat %s | grep ens_fromid | sort -n -r -k 3 | awk -v max=%s \'{print $2, $3/max}\' | head -100 | tr \'\n\' \',\' | tr \' \' \':\' >> %s'},
        "cs_keyword": {'name': '关键字',
                       'max': 0,
                       'format_script': 'cat %s | grep cs_keyword | sort -n -r -k 3 |  awk -v max=%s \'{print $2, $3/max}\' | head -100 | tr \'\n\' \',\' | tr \' \' \':\' >> %s'},
        "os": {'name': '操作平台',
               'max': 0,
               'format_script': 'cat %s | grep \'^os\' | awk \'{print $2, $3}\' | sort -n -r -k 2 >> %s'}
    }
    #读取每一行，以制表符分割，读取0位置匹配orderkeys中的数据，读取2位置匹配max，并选取最大的替换成max的value
    # 如果自己生成txt文件测试，请在file->default setings->edit->code style->other file typez中
    # 勾选TAB键制表符的功能，即勾选Use tab character
    with open(input_file, 'r') as fr:
        lines = fr.readlines()
        for line in lines:
            format_map[line.split('\t')[0]]['max'] = max(format_map[line.split('\t')[0]]['max'],
                                                         int(line.split('\t')[2]))

    output_file = input_file.split('/')[2].split('.')[0] + '_用户画像.txt'
    run_command('echo "----------用户画像----------" > %s ' % (output_file))
    for key in ordered_keys:
        #输出每个画像属性名称
        run_command('echo "\n******%s******" >> %s ' % (format_map[key]['name'], output_file))
        #分类执行脚本
        if key in ('ens_ct', 'ens_sct', 'ens_fromid', 'cs_keyword'):
            run_command(format_map[key]['format_script'] % (input_file, format_map[key]['max'], output_file))
        else:
            run_command(format_map[key]['format_script'] % (input_file, output_file))
    return output_file


if __name__ == '__main__':
    input = sys.argv[1]
    format_output_file(input)
