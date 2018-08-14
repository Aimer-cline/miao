from scrapy import Selector
from scrapy import Request
from miao.items import MiaoItem
import scrapy


class MiaoSpider(scrapy.Spider):
    name = "miao"
    host = "http://tieba.baidu.com/"
    start_urls = [
        'https://tieba.baidu.com/f?kw=%E6%8A%97%E5%8E%8B&ie=utf-8&pn=0'
    ]

    def get_next_url(self, start_urls):
        l = start_urls.split('=')
        oldid = int(l[3])
        newid = oldid + 50
        if newid == 1727800:
            return
        newurl = l[0] + '=' + l[1] + '=' + l[2] + '=' + str(newid)
        return str(newurl)

    def start_requests(self):
        yield Request(self.start_urls[0],callback=self.parse_page)

    def parse_page(self, response):
        selector = Selector(response)
        content_list = selector.xpath("//a[@class='j_th_tit ']")
        for content in content_list:
            topic = content.xpath('string(.)').extract_first()
            url = self.host + content.xpath('@href').extract_first()
            item = MiaoItem()
            item["url"] = url
            item["topic"] = topic
            yield Request(url=url, callback=self.parse_topic)
        next_url = self.get_next_url(response.url)
        yield Request(next_url,callback=self.parse_page)

    def parse_topic(self, response):
        selector = Selector(response)
        contest_list = selector.xpath("//div[@class='d_post_content j_d_post_content ']")
        for content in contest_list:
            content = content.xpath('string(.)').extract_first()
            item = MiaoItem()
            item["content"] = content
            yield item