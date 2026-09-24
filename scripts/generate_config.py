# -*- coding:utf-8 -*-


import json
import os



BASE=os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)



OUT=os.path.join(
    BASE,
    "output"
)




def save(name,data):


    path=os.path.join(
        OUT,
        name
    )


    with open(

        path,

        "w",

        encoding="utf8"

    ) as f:


        json.dump(

            data,

            f,

            ensure_ascii=False,

            indent=2

        )




def generate(data):


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
            "MyTVYuan",

            "url":
            "tvbox.json"

            }

        ]

        }

    )
