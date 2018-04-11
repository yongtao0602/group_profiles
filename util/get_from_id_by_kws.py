# -*- coding: utf-8 -*-

import json
import urllib2
import urllib
from urllib import urlencode


def get_from_id_by_kws(kws):
    url = 'http://lc1.haproxy.yidian.com:8902/service/assistant?' + urlencode({'word': kws})

    print url
    res = urllib.urlopen(url).read()
    from_id = json.loads(res)['channels'][0]['id']
    return from_id


def get_from_id_by_kws_list(kws_list):
    return map(get_from_id_by_kws, kws_list.split('&&'))


if __name__ == '__main__':
    print get_from_id_by_kws_list('互联网&&技术')
