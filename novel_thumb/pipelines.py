# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os 

import requests


class NovelThumbPipeline(object):
    # def __init__(self):
    def process_item(self, item, spider):
        category_id = item.get('category_id', '')
        article_url_base = item.get('article_url_base', '')
        thumb = item.get('thumb', '')
        allowed_domain = item.get('allowed_domain', '')

        temp = article_url_base.split('/')
        chapter_url_base = temp[1] if temp else "temp"
        cur_path = "/volume/novel_context" + os.path.sep + allowed_domain
        target_path = cur_path + os.path.sep + chapter_url_base
        filename_path = cur_path + os.path.sep + \
                        "thumb" + os.path.sep + chapter_url_base + ".jpg"

        r = requests.get(thumb,stream=True)

        if not os.path.exists(target_path):
            os.makedirs(target_path)
        with open(filename_path, 'wb') as f:
            for chunk in r.iter_content():
                f.write(chunk)
        return item
