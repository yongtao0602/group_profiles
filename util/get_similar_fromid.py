# -*- coding: utf-8 -*-

import sys
import requests
from urllib2 import urlopen
from urllib import urlencode
import json

reload(sys)
sys.setdefaultencoding("utf-8")

KEY_TO_FROM_ID = 'http://dataplatform.yidian.com:8083/api/other/channel_query/query_all'
FROM_ID_SIMILAR = 'http://10.111.0.129:3303/info'


def get_fromid_from_keyword(keyword):
    (fromid, name) = requests.post(KEY_TO_FROM_ID, data={
        'word': keyword
    }).text.split(',')[0].split('-')
    return fromid, name


def get_similar_from_id(from_id):
    query = {
        'method': 'cbow',
        'interest': 'fromid:%s' % from_id
    }
    json_result = json.loads(urlopen('%s?%s' % (FROM_ID_SIMILAR, urlencode(query))).read())
    if json_result['status'] == 'success':
        for item in json_result['result']:
            print '%s\t%f' % (item['name'], item['value'])


if __name__ == '__main__':
    keyword = sys.argv[1]
    from_id, name = get_fromid_from_keyword(keyword)
    print 'from_id=%s 频道名=%s' % (from_id, name)
    print '----------------------------------'
    get_similar_from_id(from_id)

