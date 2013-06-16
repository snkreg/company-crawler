import random
from os import path
from scrapy.conf import settings
from scrapy import log


class ProxyEvaluator(object):
    MIN_ATTEMPTS = settings['MIN_ATTEMPTS']

    def __init__(self):
        self._proxy_stats = {}
        proxy_path = settings['PROXY_FILE_PATH']
        if proxy_path is None:
            self._disabled = True
            log.msg("No proxy list provided. Proxy disabled")
        else:
            self._disabled = False
            f = open(proxy_path)
            self._proxy_list = f.readlines()
            f.close()
            for proxy in self._proxy_list:
                proxy = proxy.rstrip('\r\n')
                self._proxy_stats[proxy] = (0, 0)

            self._previous_selections = None
            self._discarded = {}
            log.msg("Proxy list path=%s" % proxy_path)

    def inc_failure(self, key):
        """Increments the number of detected
        failures for the given ip:port in key
        """
        suc, fail = self._proxy_stats[key]
        self._proxy_stats[key] = (suc, fail + 1)

    def inc_successes(self, key):
        """Increments the number of detected
        sucesses for the given ip:port in key
        """
        suc, fail = self._proxy_stats[key]
        self._proxy_stats[key] = (suc + 1, fail)

    def get_stats(self, key):
        """ Returns a pair (succeses, failures)
        for a given key (ip:port)
        """
        return self._proxy_stats[key]

    def _should_use_proxy(self, key):
        if key == self._previous_selections:
            return False

        suc, fail = self._proxy_stats[key]
        total_conn = suc + fail
        if fail >= ProxyEvaluator.MIN_ATTEMPTS:
            self._discarded[key] = self._proxy_stats[key]
            log.msg("Discarded proxy [%s]" % key)
            del(self._proxy_stats[key])
            return False

        return True

    def valid_proxy(self):
        """
        Return a valid proxy (a string in the
        form ip:port)
        """
        p = random.choice(self._proxy_stats.keys())
        while not self._should_use_proxy(p):
            p = random.choice(self._proxy_stats.keys())

        self._previous_selections = p
        return p

    def is_disabled(self):
        """Returns whether the proxy selector
        is disabled or not
        """
        return self._disabled
