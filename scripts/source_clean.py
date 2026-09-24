# -*- coding:utf-8 -*-



def clean(sites):


    result=[]


    cache=set()



    for s in sites:


        name=s.get(
            "name"
        )


        api=s.get(
            "api"
        )



        if not name or not api:

            continue



        if api in cache:

            continue



        speed=s.get(
            "speed",
            0
        )


        if speed<=0:

            continue



        cache.add(
            api
        )


        result.append(
            s
        )


    return result
