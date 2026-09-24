import os
import json
import time


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


def main():

    print("======================")
    print("MyTVYuan V8 Start")
    print("======================")


    output = os.path.join(
        BASE_DIR,
        "output"
    )


    if not os.path.exists(output):

        os.makedirs(output)


    data = {

        "version":"8.0",

        "update_time":
            time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "spider":"ok",

        "sites":[]

    }


    file = os.path.join(
        output,
        "tvbox.json"
    )


    with open(
        file,
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
        file
    )



if __name__=="__main__":

    main()
