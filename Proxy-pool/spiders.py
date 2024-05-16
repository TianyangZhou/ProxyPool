"""
爬虫模块，包含爬虫类的元类、基类、异常类
如果用户需要定义自己的爬虫类，必须要继承`SpiderMeta`元类和`BaseSpider`基类，
并重写`get`方法，方法需要返回`ip:port`字符串组成的列表形式的代理。
"""

from request import PageRequest
from bs4 import BeautifulSoup
import logging
import time
from lxml import html


class SpiderMeta(type):
    spiders = []
    def __new__(cls, *args, **kwargs):
        cls.spiders.append(super().__new__(cls, *args, **kwargs))
        return super().__new__(cls, *args, **kwargs)


class BaseSpider(object):
    def __init__(self):
        self._counter = 1
        self._request = PageRequest()
        self._logger = logging.getLogger('root')

    def increment(self, count):
        """子类用于增加计数器的方法
        :param count: 计数器增加量
        :return: None
        """
        self._counter += count

    def flush(self):
        """将计数器刷新为 1
        :return: None
        """
        self._counter = 1

    def get(self, step=1):
        """爬虫类必须有get方法，其中包含爬虫代码
        :param step: 每次爬取页数，如一次没有充足，会继续累加，充足则复位
        :return: 包含 IP:Port 字符串格式的列表
        """
        raise RewriteSpiderError(__class__.__name__)


class RewriteSpiderError(Exception):
    """自定义异常， 提醒用户按照规定重写方法"""
    def __init__(self, cls_name):
        super().__init__(self)
        self.cls_name = cls_name

    def __str__(self):
        return repr(f'爬虫"{self.cls_name}"没有重写get方法')


class XiciSpider(BaseSpider, metaclass=SpiderMeta):
    start_url = 'https://cn.proxy-tools.com/proxy/us?page={}'

    def get(self, step=1):
        urls = [self.start_url.format(page) for page in range(self._counter, self._counter+step)]
        proxies = []
        for url in urls:
            response = self._request.get_resp(url)
            print(response.url)
            while response.status_code == 503:
                self._logger.debug('%s 被反爬，开始使用代理' %
                                   self.__class__.__name__)
                self._request.load_proxy()
                time.sleep(5)
                response = self._request.get_resp(url)
            tree = html.fromstring(response.text)
            # XPath to select the rows in the table
            rows = tree.xpath('/html/body/div[1]/main/table/tbody/tr')

            # Initialize an empty list to store proxies
            proxies = []

            # Iterate over the rows, starting from the second row (index 1)
            for row in rows[1:]:
                ip = row.xpath('td[1]/text()')[0]
                port = 80
                proxies.append(f'{ip}:{port}')
            print(proxies)
            time.sleep(5)
        self._counter += step
        self._logger.debug('爬虫{}抓取了{}个代理'.format(self.__class__.__name__, len(proxies)))
        return proxies







