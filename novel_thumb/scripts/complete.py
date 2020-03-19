# -*- coding: utf-8 -*-

import os

import pymysql
import requests

conn = pymysql.connect(host='47.244.114.115', user='root', port=3306,
                                    passwd='Fik2mcKWThRbEFyx', db='distributed_spider', charset='utf8')

cur = conn.cursor()


def complete():
    sql = "SELECT id, thumb, pinyin FROM `articles` where thumb like 'http%' order by id"
    cur.execute(sql)
    result = cur.fetchall()
    for res in result:
        print(res)
        # id = res.get("id", 0)
        # url = res.get("thumb", "")
        # pinyin = res.get("pinyin", "")
        id = res[0]
        url = res[1]
        pinyin = res[2]
        print(id)

        r = requests.get(url, stream=True)
        if r.status_code != 404:
            target_path = "/volume/novel_context" + os.path.sep + "35kushu.com" + os.path.sep + "thumb"
            filename_path = target_path + os.path.sep + pinyin + ".jpg"
            with open(filename_path, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)

            sql_1 = "update articles set thumb=%s where id=%s"
            cur.execute(sql_1, (filename_path, id))
            cur.connection.commit()


if __name__=="__main__":
    complete()
