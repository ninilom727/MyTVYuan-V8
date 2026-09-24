# -*- coding:utf-8 -*-


FIXED=[

"索尼",

"360"

]




def rank(sites):


    top=[]

    other=[]



    for s in sites:


        name=s.get(
            "name",
            ""
        )


        if any(

            x in name

            for x in FIXED

        ):


            top.append(
                s
            )

        else:

            other.append(
                s
            )



    other.sort(

        key=lambda x:

        x.get(
            "speed",
            0
        ),

        reverse=True

    )



    return top+other
