#!/usr/bin/env python3

import requests
from addict import Dict
import sqlite3
import urllib
import hashlib
import json
import os

db = "/tmp/micro_utils_db"

con = sqlite3.connect(db)
cur = con.cursor()
cur.execute(
    "create table IF NOT EXISTS  gps_baidu_cache (gps, gps_data)")
cur.execute(
    "CREATE INDEX IF NOT EXISTS  gps_index on gps_baidu_cache (gps)")
con.close()

# 百度 拾取坐标 http://api.map.baidu.com/lbsapi/getpoint/index.html


def clear_cache():
    os.remove(db)


def get_sn(query_str, sk):

    # 改编自： https://lbsyun.baidu.com/index.php?title=lbscloud/api/appendix
    # 对queryStr进行转码，safe内的保留字符不转换
    encoded_str = urllib.parse.quote(query_str, safe="/:=&?#+!$,;'@()*[]")
    # 在最后直接追加上yoursk
    raw_str = f'{encoded_str}{sk}'
    return hashlib.md5(urllib.parse.quote_plus(raw_str).encode('utf8')).hexdigest()


def get_address_no_cache(lat, lng, ak, sk):
    query_str = f'/reverse_geocoding/v3/?ak={ak}&output=json&coordtype=wgs84ll&location={lat},{lng}'
    sn = get_sn(query_str=query_str, sk=sk)
    url = f'http://api.map.baidu.com{query_str}&sn={sn}'

    res = requests.get(url)
    return res.text


def get_address_from_cache(lat, lng):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(
        "SELECT gps_data FROM gps_baidu_cache where gps=?", (f'{lat},{lng}',))
    gps_data = cur.fetchone()
    con.close()

    if gps_data is not None:
        return gps_data[0]

    return None


def set_address_to_cache(lat, lng, gps_data):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(
        "insert into gps_baidu_cache values(?,?)", (f'{lat},{lng}', gps_data,))
    con.commit()
    con.close()


def get_address(location, ak, sk):
    lat, lng = location

    gps_data = get_address_from_cache(lat=lat, lng=lng)

    if(gps_data is None):
        gps_data = get_address_no_cache(lat, lng, ak, sk)
        set_address_to_cache(lat, lng, gps_data)

    # return Dict(json.loads(gps_data))
    return gps_data
