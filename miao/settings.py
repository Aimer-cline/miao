BOT_NAME = 'miao'

SPIDER_MODULES = ['miao.spiders']
NEWSPIDER_MODULE = 'miao.spiders'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {'miao.pipelines.MiaoPipeline': 400,
}