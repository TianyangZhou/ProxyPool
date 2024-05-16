from flask import Flask, jsonify
import redis
import random

app = Flask(__name__)

# 连接到 Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, password='Aa987987.', db=8)


@app.route('/get_proxy', methods=['GET'])
def get_proxy():
    # 获取所有代理 IP 地址
    proxy_ips = list(redis_client.smembers("proxy:ips"))

    # 随机选择一个代理
    if proxy_ips:
        proxy_data = random.choice(proxy_ips).decode()  # 确保解码为字符串
        proxy_info = {
            "proxy": proxy_data
        }
        return jsonify(proxy_info)
    else:
        return jsonify({"error": "No proxies available"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
