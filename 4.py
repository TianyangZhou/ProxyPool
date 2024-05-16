import requests

# 获取代理 IP 地址
proxy_service_url = "http://127.0.0.1:5000/get_proxy"
response = requests.get(proxy_service_url)
proxy_data = response.json()
print(proxy_data)
if "proxy" in proxy_data:
    proxy_ip = proxy_data["proxy"]
    proxies = {
        "http": f"{proxy_ip}",
        "https": f"{proxy_ip}"
    }
    print(proxies)

    # 要访问的目标网页
    target_url = "https://dev.kdlapi.com/testproxy"

    # 使用代理发送请求
    try:
        response = requests.get(target_url, proxies=proxies)

        # 打印响应内容
        print("状态码:", response.status_code)
        print("响应内容:", response.text)
    except requests.RequestException as e:
        print(f"请求发生错误: {e}")
else:
    print("无法获取代理 IP 地址")
