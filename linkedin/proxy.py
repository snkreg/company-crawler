import random

PROXIES = open('/home/doc/workspace/linkedin/linkedin/goodproxy.txt').readlines()

class ProxyEvaluator(object):
    MIN_CONN = 1

    def __init__(self):
        self._proxy_stats = {}
        for proxy in PROXIES:
            self._proxy_stats[proxy] = (0,0)

        self._previous_selections = None
        self._discarded = {}

    def inc_failure(self, key):
        suc, fail = self._proxy_stats[key]
        self._proxy_stats[key] = (suc, fail + 1)

    def inc_successes(self, key):
        suc, fail = self._proxy_stats[key]
        self._proxy_stats[key] = (suc + 1, fail)

    def get_stats(self, key):
        return self._proxy_stats[key]

    def _should_use_proxy(self, key):
        if key == self._previous_selections:
            return False

        suc, fail = self._proxy_stats[key]
        total_conn = suc + fail
        if total_conn > ProxyEvaluator.MIN_CONN and fail / total_conn > 0.5:
            self._discarded[key] = self._proxy_stats[key]
            del(self._proxy_stats[key])
            return False

        return True

    def valid_proxy(self):
        p = random.choice(PROXIES)
        while not self._should_use_proxy(p):
            p = random.choice(PROXIES)

        self._previous_selections = p
        return p



