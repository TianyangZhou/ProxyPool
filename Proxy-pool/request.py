from config import HEADERS
from dbredis import RedisOperator
from requests.exceptions import ProxyError, ConnectionError, Timeout, ChunkedEncodingError
import requests
import logging


class PageRequest(object):
    def __init__(self):
        self.proxies_arg = None
        self._logger = logging.getLogger('root')
        self._headers = HEADERS
        self._pool = RedisOperator()

    def get_resp(self, url, retry=2):
        try:
            return requests.get(url, headers=self._headers, timeout=20, proxies=self.proxies_arg)
        except(ProxyError, ConnectionError, Timeout, ChunkedEncodingError):
            if retry > 0:
                return self.get_resp(url, retry-1)
            self._logger.warning('爬虫可能被反爬，正在加载代理重试')
            self.load_proxy()
            return self.get_resp(url)



    def load_proxy(self):
        self.proxies_arg = {'http': self._pool.get()}

