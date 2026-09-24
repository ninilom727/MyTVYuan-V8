# -*- coding:utf-8 -*-

import json
import os
import time


BASE = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


OUT = os.path.join(
    BASE,
    "output"
)



def save(name, data):

    path = os.path.join(
        OUT,
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




def add_info(data):

    """
    增加统计信息
    """

    data["update_time"] = time.strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    data["source_count"] = len(
        data.get(
            "sites",
            []
        )
    )


    data["parse_count"] = len(
        data.get(
            "parses",
            []
        )
    )


    data["live_count"] = len(
        data.get(
            "lives",
            []
        )
    )


    return data




def generate(data):


    data = add_info(
        data
    )


    save(
        "tvbox.json",
        data
    )


    save(
        "tvbox_full.json",
        data
    )


    save(
        "tvbox_multi.json",
        {

            "urls":[

                {

                    "name":
                    "MyTVYuan V8",

                    "url":
                    "https://raw.githubusercontent.com/ninilom727/MyTVYuan-V8/main/output/tvbox.json"

                }

            ]

        }
    )
