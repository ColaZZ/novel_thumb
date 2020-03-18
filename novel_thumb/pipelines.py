# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os 

import requests
import pymysql


class NovelThumbPipeline(object):
    def __init__(self):
        # self.conn = pymysql.connect(host='127.0.0.1', user='root',
        #                             passwd='123456', db='distributed_spider', charset='utf8')
        self.conn = pymysql.connect(host='47.244.114.115', user='root', port=3306,
                                    passwd='Fik2mcKWThRbEFyx', db='distributed_spider', charset='utf8')
        self.cur = self.conn.cursor()



    def process_item(self, item, spider):
        category_id = item.get('category_id', '')
        article_url_base = item.get('article_url_base', '')
        thumb = item.get('thumb', '')
        allowed_domain = item.get('allowed_domain', '')

        temp = article_url_base.split('/')
        chapter_url_base = temp[1] if temp else "temp"
        cur_path = "/volume/novel_context" + os.path.sep + allowed_domain
        # cur_path = "/mnt/d"
        target_path = cur_path + os.path.sep + "thumb"
        filename_path = cur_path + os.path.sep + \
                        "thumb" + os.path.sep + chapter_url_base + ".jpg"

        if thumb:
            thumb_path = filename_path
        else:
            thumb_path = ""


        sql = "update articles set thumb=%s where pinyin=%s"
        self.cur.execute(sql, (filename_path, chapter_url_base))
        self.cur.connection.commit()


        r = requests.get(thumb,stream=True)

        if r.status_code != 404 and thumb_path:
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            with open(filename_path, 'wb') as f:
                for chunk in r.iter_content():
                    f.write(chunk)

        return item
