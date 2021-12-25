#!/usr/bin/env python3

import requests
from addict import Dict

# 百度 拾取坐标 http://api.map.baidu.com/lbsapi/getpoint/index.html

def get_sn(query_str, sk):
    import urllib
    import hashlib
    # 改编自： https://lbsyun.baidu.com/index.php?title=lbscloud/api/appendix
    # 对queryStr进行转码，safe内的保留字符不转换
    encoded_str = urllib.parse.quote(query_str, safe="/:=&?#+!$,;'@()*[]")
    # 在最后直接追加上yoursk
    raw_str = f'{encoded_str}{sk}'
    return hashlib.md5(urllib.parse.quote_plus(raw_str).encode('utf8')).hexdigest()


def get_address(location, ak, sk):
    lat, lng = location
    query_str = f'/reverse_geocoding/v3/?ak={ak}&output=json&coordtype=wgs84ll&location={lat},{lng}'
    sn = get_sn(query_str=query_str, sk=sk)
    url = f'http://api.map.baidu.com{query_str}&sn={sn}'

    res = requests.get(url)
    return Dict(res.json())
