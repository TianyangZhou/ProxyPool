import requests

# 隧道域名:端口号
tunnel = "as.bd43252f4297b573.ipmars.vip:4900"

# 用户名密码方式
username = "gNEDFsUpc4-zone-mars-region-JP"
password = "51668746"
proxies = {
    "http": "socks5h://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
    "https": "socks5h://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
}

# 白名单方式（需提前设置白名单）
# proxies = {
#     "http": "socks5://%(proxy)s/" % {"proxy": tunnel},
#     "https": "socks5://%(proxy)s/" % {"proxy": tunnel}
# }

# 要访问的目标网页
target_url = "https://dev.kdlapi.com/testproxy"

# 使用隧道域名发送请求
response = requests.get(target_url, proxies=proxies)

# 获取页面内容
if response.status_code == 200:
    print(response.text)  # 请勿使用keep-alive复用连接(会导致隧道不能切换IP)
