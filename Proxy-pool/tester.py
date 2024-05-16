import asyncio
import aiohttp
import logging
from config import HEADERS, TEST_API
from dbredis import RedisOperator



class UsabilityTester(object):
    """代理测试器，负责检验给定代理的可用性"""
    def __init__(self):
        self._headers = HEADERS
        self._logger = logging.getLogger('root')
        self.test_api = TEST_API
        self._pool = RedisOperator()

    async def test_signal_proxy(self, proxy):
        """异步测试单个代理"""
        async with aiohttp.ClientSession() as sess:
            real_proxy = 'http://'+proxy
            try:
                async with sess.get(self.test_api, headers=self._headers, proxy=real_proxy, timeout=10, allow_redirects=False):
                    self._pool.increase(proxy)
            except (asyncio.TimeoutError, Exception):
                self._pool.decrease(proxy)


    def test(self, proxies):
        """测试传入的代理列表，
        将在定时测试周期和每次爬虫工作后被调用
        :param proxies: 代理列表
        :return: None
        """
        self._logger.info('测试器开始工作，本次测试 %s 个代理' % len(proxies))
        loop = asyncio.get_event_loop()
        for batch in [proxies[i: i+200] for i in range(0, len(proxies), 200)]:
            tasks = [self.test_signal_proxy(proxy) for proxy in batch]
            loop.run_until_complete(asyncio.wait(tasks, loop=loop))


