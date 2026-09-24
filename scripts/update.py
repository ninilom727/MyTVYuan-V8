#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MyTVYuan V8

自动更新主程序

流程:

sources.txt
      |
      ↓
fetch json
      |
      ↓
merge
      |
      ↓
speed test
      |
      ↓
clean
      |
      ↓
rank
      |
      ↓
generate

输出:

tvbox.json
tvbox_full.json
tvbox_multi.json

"""


import os
import sys
import json
import time
import requests


# 当前目录加入路径

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


SCRIPT_DIR = os.path.join(
    BASE_DIR,
    "scripts"
)


sys.path.append(
    SCRIPT_DIR
)



# 导入模块

try:

    from source_speed import add_speed

    from source_rank import rank

    from source_clean import clean

    from generate_config import generate


except Exception as e:

    print(
        "模块加载失败:",
        e
    )

    sys.exit(1)



CONFIG_DIR=os.path.join(
    BASE_DIR,
    "config"
)



SOURCE_FILE=os.path.join(
    CONFIG_DIR,
    "sources.txt"
)



TIMEOUT=15



HEADERS={

    "User-Agent":

    "Mozilla/5.0 MyTVYuan-V8"

}




# =========================
# 初始化
# =========================


def init():


    output=os.path.join(

        BASE_DIR,

        "output"

    )


    if not os.path.exists(output):

        os.makedirs(output)




# =========================
# 读取源列表
# =========================


def load_sources():


    if not os.path.exists(
        SOURCE_FILE
    ):


        print(
            "缺少:",
            SOURCE_FILE
        )

        return []



    urls=[]


    with open(

        SOURCE_FILE,

        "r",

        encoding="utf-8"

    ) as f:


        for line in f:


            url=line.strip()



            if not url:

                continue



            if url.startswith("#"):

                continue



            urls.append(url)



    return urls





# =========================
# 请求JSON
# =========================


def fetch_json(url):


    try:


        print(
            "抓取:",
            url
        )



        r=requests.get(

            url,

            headers=HEADERS,

            timeout=TIMEOUT

        )



        if r.status_code != 200:

            print(

                "HTTP",

                r.status_code

            )

            return None



        return r.json()



    except Exception as e:


        print(

            "失败:",

            e

        )

        return None






# =========================
# 合并配置
# =========================


def merge(configs):


    result={


        "spider":"",

        "sites":[],

        "parses":[],

        "lives":[]

    }



    for cfg in configs:


        if not isinstance(
            cfg,
            dict
        ):

            continue



        spider=cfg.get(
            "spider"
        )


        if spider:

            result["spider"]=spider




        for key in [

            "sites",

            "parses",

            "lives"

        ]:


            value=cfg.get(
                key,
                []
            )


            if isinstance(
                value,
                list
            ):


                result[key].extend(
                    value
                )



    return result





# =========================
# 去重基础处理
# =========================


def duplicate_clean(items):


    result=[]


    cache=set()



    for item in items:


        if not isinstance(
            item,
            dict
        ):

            continue



        key=item.get(
            "key"
        )



        if not key:

            key=item.get(
                "name"
            )



        if key in cache:

            continue



        cache.add(
            key
        )


        result.append(
            item
        )



    return result





# =========================
# 主程序
# =========================


def main():


    print("\n")

    print(
        "="*60
    )

    print(
        " MyTVYuan V8 Update Start "
    )

    print(
        time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    print(
        "="*60
    )



    init()



    urls=load_sources()



    print(

        "配置源数量:",

        len(urls)

    )



    configs=[]



    for url in urls:


        data=fetch_json(
            url
        )



        if data:


            configs.append(
                data
            )



    print(

        "成功获取:",

        len(configs)

    )



    if not configs:


        print(
            "没有有效配置"
        )

        return



    # 合并


    merged=merge(
        configs
    )



    print(

        "原始站点:",

        len(
            merged["sites"]
        )

    )



    # 基础去重


    merged["sites"]=duplicate_clean(
        merged["sites"]
    )


    merged["parses"]=duplicate_clean(
        merged["parses"]
    )


    merged["lives"]=duplicate_clean(
        merged["lives"]
    )



    print(

        "去重后:",

        len(
            merged["sites"]
        )

    )



    # =====================
    # 播放测速
    # =====================


    try:


        merged["sites"]=add_speed(

            merged["sites"]

        )


    except Exception as e:


        print(

            "测速失败:",

            e

        )





    # =====================
    # 清洗
    # =====================


    try:


        merged["sites"]=clean(

            merged["sites"]

        )


    except Exception as e:


        print(

            "清洗失败:",

            e

        )





    # =====================
    # 排序
    # =====================


    try:


        merged["sites"]=rank(

            merged["sites"]

        )


    except Exception as e:


        print(

            "排序失败:",

            e

        )





    # =====================
    # 输出
    # =====================


    generate(
        merged
    )



    print(

        "="*60

    )

    print(

        " MyTVYuan V8 更新完成 "

    )

    print(

        "="*60

    )






if __name__=="__main__":

    main()
