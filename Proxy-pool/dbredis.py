from config import HOST, PORT, DB, POOL_NAME, INIT_SCORE, REGULATE_SCORE
from random import choice, choices
import redis
import logging

class RedisOperator(object):
    def __init__(self):
        self._conn = redis.StrictRedis(
            host=HOST,
            port=PORT,
            db=DB,
            password='Aa987987.',
            max_connections=20,
            decode_responses=True
        )
        self._pool_name = POOL_NAME
        self._logger = logging.getLogger('root')
        self._init_score = INIT_SCORE
        self._regulate_score = REGULATE_SCORE
        self._usable_score = self._init_score + self._regulate_score

    def add(self, proxy, score=0):
        """添加一个代理，并设置初始分数
        判断符合IP:Port格式，并且池中不存在相同的
        :param proxy: 代理
        :param score: 分数
        :return: 1 or 0
        """
        if score == 0:
            score = self._init_score
        if self._conn.sadd(proxy, 'register'):
            return self._conn.zadd(self._pool_name, {proxy: score})
        return 0

    def get(self):
        """返回随机一个可用代理
        :return: 字符串形式
        """
        return self._weight_choices()[0]

    def gets(self, total):
        """返回随机多个可用代理
        :param total: 返回的数量
        :return: 列表形式
        """
        return self._weight_choices(total)

    def get_all(self):
        """返回所有代理
        :return: 列表形式
        """
        return self._conn.zrevrangebyscore(self._pool_name, 100, 0)

    def _weight_choices(self, total=1):
        """根据分数作为相对权重，随机出指定数量的可用代理并返回
        指定多个结果可能会有重复
        :param total: 返回的数量
        :return: 列表形式
        """
        if self.usable_size < total:
            self._logger.warning('可用代理低于请求返回的数量，请降低请求数量')
        proxies = []
        scores = []
        for proxy, score in self._conn.zrevrangebyscore(self._pool_name, 100, 0, start=0, num=max(200, total), withscores=True):
            proxies.append(proxy)
            scores.append(score)
        return choices(proxies, scores, k=total)

    def get_best(self):
        """返回分数最高的随机一个代理
        :return: 字符串形式
        """
        proxies = self._conn.zrevrange(self._pool_name, 0, 1)
        if proxies:
            return choice(proxies)

    def score(self, proxy):
        """返回指定代理的分数
        :param proxy: 代理
        :return: 分数
        """
        score = self._conn.zscore(self._pool_name, proxy)
        if score:
            return score
        return 0

    def increase(self, proxy):
        """增加指定代理的分数，最高为100
        :param proxy: 代理
        :return: 修改后的分数
        """
        diff = 100 - self.score(proxy)
        if diff >= self._regulate_score:
            return self._conn.zincrby(self._pool_name, self._regulate_score, proxy)
        else:
            return self._conn.zincrby(self._pool_name, diff, proxy)

    def decrease(self, proxy):
        """减少指定代理的分数，为0则删除
        :param proxy: 代理
        :return: 修改后的分数
        """
        if self.score(proxy) > self._regulate_score:
            return self._conn.zincrby(self._pool_name, -self._regulate_score, proxy)
        else:
            return self.delete(proxy)

    def delete(self, proxy):
        """删除指定的一个代理（有重复会删除多个）
        并且将对应 key 添加5天过期时间
        :param proxy: 代理
        :return: 删除数量
        """
        self._conn.expire(proxy, 432000)
        return self._conn.zrem(self._pool_name, proxy)

    @property
    def usable_size(self):
        """返回池中可用代理总数
        :return: 整型
        """
        return self._conn.zcount(self._pool_name, self._usable_score, 100)

    @property
    def size(self):
        """返回池中所有代理总数
        :return: 整型
        """
        return self._conn.zcount(self._pool_name, 0, 100)
