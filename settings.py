BOT_NAME = 'linkedin'
LOG_LEVEL = 'DEBUG'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 542,
    'linkedin.middleware.ProxySelectorMiddleware': 543,
    'linkedin.middleware.CustomUserAgentMiddleware': 545,
}

SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.depth.DepthMiddleware': 546
}

ITEM_PIPELINES = ['linkedin.pipelines.CleanseTextPipeline',
                  'linkedin.pipelines.MongoDBPipeline']
SPIDER_MODULES = ['linkedin.spiders']
NEWSPIDER_MODULE = 'linkedin.spiders'

COOKIES_ENABLED = False
REDIRECT_ENABLED = False

RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [113, 302, 500, 502, 503, 504, 400, 403, 404, 408]

# Edit values from here

## TIME RELATED PARAMETERS
# Delay between requests (in seconds)
DOWNLOAD_DELAY = 0.5
# Number of seconds to wait until considering a request timed out
DOWNLOAD_TIMEOUT = 2

#### The following parameters can't be commented out

## STORAGE PARAMETERS
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'linkedin'
MONGODB_COLLECTION = 'companies'
MONGODB_UNIQ_KEY = '_id'


## PROXY PARAMETERS
# Absolute path where a proxy list can be found
# If you want to disable proxy usage, set this variable to None
PROXY_FILE_PATH = None
# Minimum depth required to use a proxy
MIN_LEVEL_FOR_PROXY = 0
# Chance (up to 10) to use a proxy
PROXY_CHANCE = 3
# Minimum number of failed attempts required to discard a proxy
# In this example, once a proxy has failed to answer a request, it will never
# be used again.
MIN_ATTEMPTS = 1

## CONTENT PARAMETERS
# A string that contains all the letters that will be looked up in the directory
# Each letter implies that every companie with that character at the beginning
# of its name will be retrieved.

# For example: COMPANY_LETTERS='az'
# All the companies whose name start with 'a' will be retrieved and so will be
# those who start with z.
#COMPANY_LETTERS = 'abcdefghijklmnopqrstuvwxyz'
COMPANY_LETTERS = 'z'
