# -*- coding:utf-8 -*-

import requests
import time


TIMEOUT = 10



def test_speed(url):

    """
    m3u8测速
    返回:
    speed kb/s
    """

    try:

        start=time.time()


        r=requests.get(

            url,

            timeout=TIMEOUT,

            stream=True

        )


        if r.status_code != 200:

            return 0



        total=0


        for chunk in r.iter_content(
            1024
        ):

            total+=len(chunk)


            if total>1024*200:

                break



        cost=time.time()-start


        if cost==0:

            return 0



        speed=total/cost/1024


        return round(
            speed,
            2
        )


    except:


        return 0




def add_speed(sites):


    result=[]


    for item in sites:


        url=item.get(
            "api",
            ""
        )


        speed=test_speed(
            url
        )


        item["speed"]=speed


        result.append(
            item
        )


        print(
            item.get("name"),
            speed
        )


    return result
