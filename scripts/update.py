#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MyTVYuan V8
TVBox 自动配置生成器

流程:

sources.txt
      |
      v
抓取远程配置
      |
      v
解析 JSON
      |
      v
过滤无效源
      |
      v
合并
      |
      v
生成:

tvbox.json
tvbox_full.json
tvbox_multi.json

"""


import os
import json
import time
import requests


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


CONFIG_DIR = os.path.join(
    BASE_DIR,
    "config"
)


OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)


SOURCE_FILE = os.path.join(
    CONFIG_DIR,
    "sources.txt"
)



TIMEOUT = 15



HEADERS = {

    "User-Agent":
    "Mozilla/5.0 MyTVYuan-V8"

}



# -------------------------
# 初始化目录
# -------------------------


def init():


    if not os.path.exists(
        OUTPUT_DIR
    ):

        os.makedirs(
            OUTPUT_DIR
        )



# -------------------------
# 读取源列表
# -------------------------


def load_sources():


    if not os.path.exists(
        SOURCE_FILE
    ):

        print(
            "不存在:",
            SOURCE_FILE
        )

        return []



    result=[]


    with open(
        SOURCE_FILE,
        "r",
        encoding="utf-8"
    ) as f:


        for line in f:


            url=line.strip()


            if url and not url.startswith("#"):


                result.append(url)



    return result




# -------------------------
# 下载配置
# -------------------------


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


        r.encoding="utf-8"



        if r.status_code != 200:

            return None



        return r.json()



    except Exception as e:


        print(
            "失败:",
            e
        )

        return None





# -------------------------
# 合并配置
# -------------------------


def merge_config(items):


    result={

        "spider":"",

        "sites":[],

        "parses":[],

        "lives":[]

    }



    for data in items:


        if not isinstance(
            data,
            dict
        ):

            continue



        if data.get(
            "spider"
        ):

            result["spider"]=data["spider"]



        for key in [

            "sites",

            "parses",

            "lives"

        ]:


            value=data.get(key)



            if isinstance(
                value,
                list
            ):


                result[key].extend(
                    value
                )



    return result





# -------------------------
# 清洗重复
# -------------------------


def clean(items):


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


        name=item.get(
            "name"
        )


        if not key:

            key=name



        if key in cache:

            continue



        cache.add(
            key
        )


        result.append(
            item
        )



    return result





# -------------------------
# 保存文件
# -------------------------


def save(name,data):


    path=os.path.join(

        OUTPUT_DIR,

        name

    )


    with open(

        path,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            data,

            f,

            ensure_ascii=False,

            indent=2

        )



    print(

        "生成:",

        path

    )






# -------------------------
# 主程序
# -------------------------


def main():


    print(
        "="*50
    )

    print(
        "MyTVYuan V8 Start"
    )

    print(
        time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    print(
        "="*50
    )



    init()



    urls=load_sources()



    print(

        "源数量:",

        len(urls)

    )



    configs=[]



    for url in urls:


        data=fetch_json(url)



        if data:


            configs.append(
                data
            )



    print(

        "有效配置:",

        len(configs)

    )



    merged=merge_config(
        configs
    )



    merged["sites"]=clean(
        merged["sites"]
    )



    merged["parses"]=clean(
        merged["parses"]
    )



    merged["lives"]=clean(
        merged["lives"]
    )



    # 主配置

    save(

        "tvbox.json",

        merged

    )



    # 全量

    save(

        "tvbox_full.json",

        merged

    )



    # 多仓

    save(

        "tvbox_multi.json",

        {

            "configs":

            [

                {

                "name":
                "MyTVYuan V8",

                "url":
                "https://raw.githubusercontent.com/"

                }

            ]

        }

    )



    print(
        "更新完成"
    )




if __name__=="__main__":

    main()
