# Scrapy settings for linkedin project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'linkedin'

#LOG_LEVEL = 'INFO'

DOWNLOADER_MIDDLEWARES = {
    'linkedin.middleware.ProxySelectorMiddleware': 543,
    'linkedin.middleware.CustomUserAgentMiddleware': 545,
}

ITEM_PIPELINES = ['linkedin.pipelines.CleanseTextPipeline', 'linkedin.pipelines.MongoDBPipeline']
SPIDER_MODULES = ['linkedin.spiders']
NEWSPIDER_MODULE = 'linkedin.spiders'
COOKIES_ENABLED = False
REDIRECT_ENABLED = False
DOWNLOAD_DELAY = 0.5
#AUTOTHROTTLE_ENABLES = True
DOWNLOAD_TIMEOUT = 2


MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'linkedin'
MONGODB_COLLECTION = 'companies'
MONGODB_UNIQ_KEY = '_id'

RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [113, 302, 500, 502, 503, 504, 400, 403, 404, 408]

MIN_LEVEL_FOR_PROXY = 1
PROXY_CHANCE = 3

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'linkedin (+http://www.yourdomain.com)'
