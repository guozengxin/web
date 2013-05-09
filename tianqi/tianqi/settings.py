# Scrapy settings for tianqi project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'tianqi'

SPIDER_MODULES = ['tianqi.spiders']
NEWSPIDER_MODULE = 'tianqi.spiders'

LOG_LEVEL = 'INFO'

DOWNLOAD_DELAY = 4
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tianqi (+http://www.yourdomain.com)'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.97 Safari/537.22'
ITEM_PIPELINES = ['tianqi.pipelines.TianqiPipeline']
