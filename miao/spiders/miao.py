from scrapy import Selector
from scrapy import Request
from miao.items import MiaoItem
import scrapy


class MiaoSpider(scrapy.Spider):
    name = "miao"
    host = "http://tieba.baidu.com/"
    # start_urls是我们准备爬的初始页
    start_urls = [
        'https://tieba.baidu.com/f?kw=%E6%8A%97%E5%8E%8B&ie=utf-8&pn={}'.format(i) for i in range(0, 500, 50)
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse_page)

    def parse_page(self, response):
        selector = Selector(response)
        # 在此，xpath会将所有class=topic的标签提取出来，当然这是个list
        # 这个list里的每一个元素都是我们要找的html标签
        content_list = selector.xpath("//a[@class='j_th_tit ']")
        # 遍历这个list，处理每一个标签
        for content in content_list:
            # 此处解析标签，提取出我们需要的帖子标题。
            topic = content.xpath('string(.)').extract_first()
            # 此处提取出帖子的url地址。
            url = self.host + content.xpath('@href').extract_first()
            item = MiaoItem()
            item["url"] = url
            item["topic"] = topic
            yield item
            yield Request(url=url, callback=self.parse_topic)

    def parse_topic(self, response):
        selector = Selector(response)
        contest_list = selector.xpath("//div[@class='d_post_content j_d_post_content ']")
        for content in contest_list:
            content = content.xpath('string(.)').extract_first()
            item = MiaoItem()
            item["content"] = content
            yield item