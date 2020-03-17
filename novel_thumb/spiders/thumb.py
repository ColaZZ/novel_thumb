# -*- coding: utf-8 -*-

import copy 

import scrapy
from scrapy.http import Request 

from ..items import NovelThumbItem 

CATEGORY_MAPS = {
    '玄幻奇幻': 1,
    '修真武侠': 2,
    '都市言情': 3,
    '历史军事': 4,
    '同人名著': 5,
    '游戏竞技': 6,
    '科幻灵异': 7,
    '耽美动漫': 8
}

class NovelThumb(scrapy.Spider):
    name = 'thumb'
    allowed_domains = ['35kushu.com']
    redis_key = "novel_thumb:start_urls"
    start_urls = ['https://www.35kushu.com']

    def parse(self, response):
        tag_url = response.xpath(
            '//div[@class="menu_list_id lan1"]/li/a/@href | //div[@class="menu_list_id lan1"]/li/a/text()').extract()
        tag_urls = [tag_url[i:i+2] for i in range(0, len(tag_url), 2)]

        for tu in tag_urls[:8]:
            tag_url, category = self.start_urls[0] + tu[0], tu[1]
            category_id = CATEGORY_MAPS.get(category)
            meta = {
                "category_id": copy.deepcopy(category_id),
                "category": copy.deepcopy(category)
            }

            yield Request(tag_url, meta=copy.deepcopy(meta), callback=self.parse_tag_detail)

    def parse_tag_detail(self, response):
        meta_start = response.meta
        novel_info_1 = response.xpath('//div[@id="centerl"]/div[@id="content"]/table/tr[not(@align)]')
        
        for ni1 in novel_info_1:
            tdd = ni1.xpath('td')
            
            article_url = self.start_urls[0] + tdd[0].xpath('a/@href').extract_first(default=' ')
            # article_title = tdd[0].xpath('a/text()').extract_first(default=' ')
            # lastest_url_base = self.start_urls[0] + tdd[1].xpath('a/@href').extract_first(default=' ')
            # lastest_chapter_id = lastest_url_base.split('/')[-1][:-5]

            meta = response.meta 
            # meta["article_url"] = article_url
            meta["article_url_base"] = article_url[33:]
            # meta["lastest_chapter_id"] = lastest_chapter_id
            yield Request(article_url, meta=meta, callback=self.parse_menu)
        
        next_page = response.xpath('//div[@class="pagelink"]/a[@class="next"]/@href').extract_first()
        if next_page:
            next_page = self.start_urls[0] + next_page
            yield Request(next_page, meta=meta_start, callback=self.parse_tag_detail)

    def parse_menu(self, response):
        menu_list = response.xpath('//div[@id="indexmain"]//div[@id="list"]/dl/dd/a/@title '
                                   '| //div[@id="indexmain"]//div[@id="list"]/dl/dd/a/@href '
                                   ).extract()
        head_list = response.xpath(
            '//head/meta[@property="og:description"]/@content | //head/meta[@property="og:image"]/@content'
            ).extract()
        menu_list_group = [menu_list[i:i + 4] for i in range(0, len(menu_list), 4)]

        meta = response.meta 
        meta["thumb"] = head_list[1]
        
        item = NovelThumbItem()
        item['category_id'] = response.meta.get("category_id", 0)
        item['article_url_base'] = response.meta.get("article_url_base", " ")
        item['thumb'] = response.meta.get("thumb", " ")
        item['allowed_domain'] = self.allowed_domains[0]
        print(item['thumb'])
        # yield item 

