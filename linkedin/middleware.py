from __future__ import division

from scrapy import log
from proxy import ProxyEvaluator
from agents import AGENTS
import random

from twisted.internet.error import TimeoutError as ServerTimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.internet.defer import TimeoutError as UserTimeoutError

from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message


"""
change request header nearly every time
"""


class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent

"""
An extension to retry failed requests that are potentially caused by temporary
problems such as a connection timeout or HTTP 500 error.

You can change the behaviour of this middleware by modifing the scraping settings:
RETRY_TIMES - how many times to retry a failed page
RETRY_HTTP_CODES - which HTTP response codes to retry

Failed pages are collected on the scraping process and rescheduled at the end,
once the spider has finished crawling all regular (non failed) pages. Once
there is no more failed pages to retry this middleware sends a signal
(retry_complete), so other extensions could connect to that signal.

About HTTP errors to consider:

- You may want to remove 400 from RETRY_HTTP_CODES, if you stick to the HTTP
  protocol. It's included by default because it's a common code used to
  indicate server overload, which would be something we want to retry
"""


class ProxySelectorMiddleware(object):

    # IOError is raised by the HttpCompression middleware when trying to
    # decompress an empty response
    EXCEPTIONS_TO_RETRY = (
        ServerTimeoutError, UserTimeoutError, DNSLookupError,
        ConnectionRefusedError, ConnectionDone, ConnectError,
        ConnectionLost, TCPTimedOutError,
        IOError)

    def __init__(self, settings):
        if not settings.getbool('RETRY_ENABLED'):
            raise NotConfigured
        self.max_retry_times = settings.getint('RETRY_TIMES')
        self.retry_http_codes = set(
            int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        self.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')
        self.proxy_ev = ProxyEvaluator()
        self.proxy_chance = settings.getint('PROXY_CHANCE')
        self.min_level = settings.getint('MIN_LEVEL_FOR_PROXY')

    def process_request(self, request, spider):
        if self.use_proxy(request):
            p = self.proxy_ev.valid_proxy()
            try:
                request.meta['proxy'] = "http://%s" % p
            except Exception, e:
                log.msg("Exception %s" % e, _level=log.CRITICAL)
        elif 'proxy' in request.meta:
            # Just in case we have received a request
            # with that flag set.
            if 'proxy' in request.meta:
                del(request.meta['proxy'])

    def process_response(self, request, response, spider):
        has_proxy = 'proxy' in request.meta
        if 'dont_retry' in request.meta:
            return response
        if response.status in self.retry_http_codes:
            # We should not use this proxy
            reason = response_status_message(response.status)
            if has_proxy:
                self.proxy_ev.inc_failure(request.meta['proxy'])
            return self._retry(request, reason, spider) or response
        else:  # Response was succesful
            if has_proxy:
                self.proxy_ev.inc_successes(request.meta['proxy'])
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and 'dont_retry' not in request.meta:
            return self._retry(request, exception, spider)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        if retries <= self.max_retry_times:
            log.msg(
                format="Retrying %(request)s (failed %(retries)d times): %(reason)s",
                level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            return retryreq
        else:
            log.msg(
                format="Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                level=log.DEBUG, spider=spider, request=request, retries=retries, reason=reason)

    def use_proxy(self, request):
        """
        using direct download for depth <= 2
        using proxy with probability 0.3
        """
        return False
        if "depth" in request.meta and int(request.meta['depth']) <= self.min_level:
            return False
        i = random.randint(1, 10)
        return i <= self.proxy_chance

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
