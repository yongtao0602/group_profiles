# -*- coding: utf-8 -*-

ordered_keys = ["ens_gender", "ens_age", "lbs_area", "lbs_tier", "lbs_province", "lbs_city", "os", "ens_ct", "ens_sct", "ens_fromid", "cs_keyword"]

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

with open('./file.txt', 'r') as fr:
    lines = fr.readlines()
    for line in lines:
        out0 = int(line.split('\t')[2])
        print('out0-----', out0)
        out1 = format_map[line.split('\t')[0]]['max']
        print('out1-----', out1)
        out = max(out0, out1)
        format_map[line.split('\t')[0]]['max'] = out
        print(format_map[line.split('\t')[0]]['max'])