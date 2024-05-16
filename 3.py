import redis

# 代理信息列表
proxies = [
    "lantaogg:ejUXvrHFmW@216.185.47.237:50101",
    "lantaogg:ejUXvrHFmW@216.185.46.218:50101",
    "lantaogg:ejUXvrHFmW@216.185.46.24:50101",
    "lantaogg:ejUXvrHFmW@166.1.9.43:50101",
    "lantaogg:ejUXvrHFmW@166.1.9.18:50101",
    "lantaogg:ejUXvrHFmW@166.1.9.222:50101",
    "lantaogg:ejUXvrHFmW@166.1.9.213:50101",
    "lantaogg:ejUXvrHFmW@166.1.11.161:50101",
    "lantaogg:ejUXvrHFmW@166.1.9.82:50101",
    "lantaogg:ejUXvrHFmW@194.233.150.151:50101",
    "lantaogg:ejUXvrHFmW@64.113.0.190:50101",
    "lantaogg:ejUXvrHFmW@64.113.0.228:50101",
    "lantaogg:ejUXvrHFmW@64.113.0.11:50101",
    "lantaogg:ejUXvrHFmW@50.114.106.205:50101",
    "lantaogg:ejUXvrHFmW@50.114.106.252:50101",
    "lantaogg:ejUXvrHFmW@166.88.55.169:50101",
    "lantaogg:ejUXvrHFmW@192.101.66.106:50101",
    "lantaogg:ejUXvrHFmW@193.41.68.72:50101",
    "lantaogg:ejUXvrHFmW@193.41.68.70:50101",
    "lantaogg:ejUXvrHFmW@193.41.68.109:50101",
    "lantaogg:ejUXvrHFmW@138.36.92.109:50101",
    "lantaogg:ejUXvrHFmW@154.16.150.76:50101",
    "lantaogg:ejUXvrHFmW@63.223.67.140:50101",
    "lantaogg:ejUXvrHFmW@166.1.13.136:50101",
    "lantaogg:ejUXvrHFmW@64.113.1.240:50101",
    "lantaogg:ejUXvrHFmW@64.226.156.126:50101",
    "lantaogg:ejUXvrHFmW@199.181.239.124:50101",
    "lantaogg:ejUXvrHFmW@50.114.104.40:50101",
    "lantaogg:ejUXvrHFmW@64.113.1.88:50101",
    "lantaogg:ejUXvrHFmW@193.169.219.49:50101",
    "lantaogg:ejUXvrHFmW@193.169.219.48:50101",
    "lantaogg:ejUXvrHFmW@193.169.219.68:50101",
    "lantaogg:ejUXvrHFmW@199.181.239.255:50101",
    "lantaogg:ejUXvrHFmW@154.16.150.62:50101",
    "lantaogg:ejUXvrHFmW@50.114.107.84:50101",
    "lantaogg:ejUXvrHFmW@199.181.239.253:50101",
    "lantaogg:ejUXvrHFmW@194.233.150.186:50101",
    "lantaogg:ejUXvrHFmW@216.185.46.209:50101",
    "lantaogg:ejUXvrHFmW@195.160.192.124:50101",
    "lantaogg:ejUXvrHFmW@74.80.255.137:50101",
    "lantaogg:ejUXvrHFmW@94.131.56.55:50101",
    "lantaogg:ejUXvrHFmW@166.88.55.215:50101",
    "lantaogg:ejUXvrHFmW@166.1.13.251:50101",
    "lantaogg:ejUXvrHFmW@94.131.56.233:50101",
    "lantaogg:ejUXvrHFmW@216.185.46.229:50101",
    "lantaogg:ejUXvrHFmW@193.169.218.242:50101",
    "lantaogg:ejUXvrHFmW@74.80.255.4:50101",
    "lantaogg:ejUXvrHFmW@185.228.194.159:50101",
    "lantaogg:ejUXvrHFmW@193.169.219.128:50101",
    "lantaogg:ejUXvrHFmW@185.68.245.87:50101",
    "lantaogg:ejUXvrHFmW@193.169.219.127:50101",
    "lantaogg:ejUXvrHFmW@94.131.86.161:50101",
    "lantaogg:ejUXvrHFmW@191.101.148.18:50101",
    "lantaogg:ejUXvrHFmW@50.114.106.212:50101",
    "lantaogg:ejUXvrHFmW@166.1.12.206:50101",
    "lantaogg:ejUXvrHFmW@193.169.218.221:50101",
    "lantaogg:ejUXvrHFmW@74.80.255.92:50101",
    "lantaogg:ejUXvrHFmW@185.228.194.117:50101",
    "lantaogg:ejUXvrHFmW@193.169.219.134:50101",
    "lantaogg:ejUXvrHFmW@185.175.225.105:50101",
    "lantaogg:ejUXvrHFmW@193.169.219.43:50101",
    "lantaogg:ejUXvrHFmW@50.114.106.127:50101",
    "lantaogg:ejUXvrHFmW@199.181.239.186:50101",
    "lantaogg:ejUXvrHFmW@168.196.236.79:50101",
    "lantaogg:ejUXvrHFmW@63.223.67.223:50101",
    "lantaogg:ejUXvrHFmW@23.27.3.217:50101",
    "lantaogg:ejUXvrHFmW@166.1.9.96:50101",
    "lantaogg:ejUXvrHFmW@50.114.104.58:50101",
    "lantaogg:ejUXvrHFmW@50.114.104.3:50101",
    "lantaogg:ejUXvrHFmW@185.240.120.9:50101",
    "lantaogg:ejUXvrHFmW@166.1.14.216:50101",
    "lantaogg:ejUXvrHFmW@213.170.223.192:50101",
    "lantaogg:ejUXvrHFmW@199.181.239.176:50101",
    "lantaogg:ejUXvrHFmW@185.240.121.81:50101",
    "lantaogg:ejUXvrHFmW@166.88.55.151:50101",
    "lantaogg:ejUXvrHFmW@64.226.156.12:50101",
    "lantaogg:ejUXvrHFmW@89.116.56.24:50101",
    "lantaogg:ejUXvrHFmW@50.114.104.180:50101",
    "lantaogg:ejUXvrHFmW@74.115.1.187:50101",
    "lantaogg:ejUXvrHFmW@185.68.245.247:50101",
    "lantaogg:ejUXvrHFmW@74.115.0.29:50101",
    "lantaogg:ejUXvrHFmW@64.113.0.82:50101",
    "lantaogg:ejUXvrHFmW@50.114.107.27:50101",
    "lantaogg:ejUXvrHFmW@195.160.192.210:50101",
    "lantaogg:ejUXvrHFmW@193.169.219.195:50101",
    "lantaogg:ejUXvrHFmW@193.169.219.64:50101",
    "lantaogg:ejUXvrHFmW@64.226.156.96:50101",
    "lantaogg:ejUXvrHFmW@193.169.218.246:50101",
    "lantaogg:ejUXvrHFmW@193.169.218.220:50101",
    "lantaogg:ejUXvrHFmW@166.1.15.148:50101",
    "lantaogg:ejUXvrHFmW@50.114.85.8:50101",
    "lantaogg:ejUXvrHFmW@166.1.10.176:50101",
    "lantaogg:ejUXvrHFmW@185.240.120.166:50101",
    "lantaogg:ejUXvrHFmW@194.5.148.160:50101",
    "lantaogg:ejUXvrHFmW@50.114.85.223:50101",
    "lantaogg:ejUXvrHFmW@216.185.46.156:50101",
    "lantaogg:ejUXvrHFmW@216.185.46.154:50101",
    "lantaogg:ejUXvrHFmW@50.114.104.86:50101",
    "lantaogg:ejUXvrHFmW@89.116.56.89:50101",
    "lantaogg:ejUXvrHFmW@185.68.245.170:50101",
    "lantaogg:ejUXvrHFmW@50.114.104.226:50101",
    "lantaogg:ejUXvrHFmW@63.223.67.201:50101",
    "lantaogg:ejUXvrHFmW@74.80.255.33:50101",
    "lantaogg:ejUXvrHFmW@166.1.8.241:50101",
    "lantaogg:ejUXvrHFmW@74.80.255.74:50101",
    "lantaogg:ejUXvrHFmW@74.80.255.75:50101",
    "lantaogg:ejUXvrHFmW@185.240.121.227:50101",
    "lantaogg:ejUXvrHFmW@185.228.195.77:50101",
    "lantaogg:ejUXvrHFmW@64.113.1.87:50101",
    "lantaogg:ejUXvrHFmW@185.68.245.20:50101",
    "lantaogg:ejUXvrHFmW@64.226.156.157:50101",
    "lantaogg:ejUXvrHFmW@216.185.46.212:50101",
    "lantaogg:ejUXvrHFmW@64.113.0.37:50101",
    "lantaogg:ejUXvrHFmW@193.169.218.84:50101",
    "lantaogg:ejUXvrHFmW@166.88.55.146:50101",
    "lantaogg:ejUXvrHFmW@74.115.1.94:50101",
    "lantaogg:ejUXvrHFmW@50.114.105.125:50101",
    "lantaogg:ejUXvrHFmW@166.1.9.39:50101",
    "lantaogg:ejUXvrHFmW@185.240.121.12:50101",
    "lantaogg:ejUXvrHFmW@194.233.150.55:50101",
    "lantaogg:ejUXvrHFmW@199.181.239.168:50101",
    "lantaogg:ejUXvrHFmW@50.114.107.57:50101",
    "lantaogg:ejUXvrHFmW@64.226.156.226:50101",
    "lantaogg:ejUXvrHFmW@166.1.11.253:50101",
    "lantaogg:ejUXvrHFmW@95.164.145.77:50101",
    "lantaogg:ejUXvrHFmW@94.124.161.202:50101",
    "lantaogg:ejUXvrHFmW@2.59.60.189:50101",
    "lantaogg:ejUXvrHFmW@200.10.35.167:50101",
    "lantaogg:ejUXvrHFmW@2.59.60.249:50101",
    "lantaogg:ejUXvrHFmW@166.88.55.113:50101",
    "lantaogg:ejUXvrHFmW@81.29.144.16:50101",
    "lantaogg:ejUXvrHFmW@50.114.106.236:50101",
    "lantaogg:ejUXvrHFmW@68.67.198.27:50101",
    "lantaogg:ejUXvrHFmW@185.240.120.208:50101",
    "lantaogg:ejUXvrHFmW@50.114.105.102:50101",
    "lantaogg:ejUXvrHFmW@108.165.219.11:50101",
    "lantaogg:ejUXvrHFmW@63.223.67.246:50101",
    "lantaogg:ejUXvrHFmW@63.223.67.128:50101",
    "lantaogg:ejUXvrHFmW@213.170.223.227:50101",
    "lantaogg:ejUXvrHFmW@50.114.104.59:50101",
    "lantaogg:ejUXvrHFmW@216.185.46.213:50101",
    "lantaogg:ejUXvrHFmW@74.80.255.195:50101",
    "lantaogg:ejUXvrHFmW@89.116.56.141:50101",
    "lantaogg:ejUXvrHFmW@181.215.184.215:50101",
    "lantaogg:ejUXvrHFmW@63.223.67.210:50101",
    "lantaogg:ejUXvrHFmW@94.124.161.9:50101",
    "lantaogg:ejUXvrHFmW@50.114.85.179:50101",
    "lantaogg:ejUXvrHFmW@216.185.46.80:50101",
    "lantaogg:ejUXvrHFmW@45.152.177.180:50101",
    "lantaogg:ejUXvrHFmW@45.152.177.94:50101",
    "lantaogg:ejUXvrHFmW@216.185.47.134:50101",
    "lantaogg:ejUXvrHFmW@216.185.47.110:50101",
    "lantaogg:ejUXvrHFmW@45.152.177.71:50101",
    "lantaogg:ejUXvrHFmW@194.233.150.83:50101",
    "lantaogg:ejUXvrHFmW@199.181.239.138:50101",
    "lantaogg:ejUXvrHFmW@199.181.239.126:50101",
    "lantaogg:ejUXvrHFmW@89.116.56.187:50101",
    "lantaogg:ejUXvrHFmW@74.115.1.193:50101",
    "lantaogg:ejUXvrHFmW@63.223.67.85:50101",
    "lantaogg:ejUXvrHFmW@194.5.148.132:50101",
    "lantaogg:ejUXvrHFmW@94.124.161.158:50101",
    "lantaogg:ejUXvrHFmW@94.124.161.133:50101",
    "lantaogg:ejUXvrHFmW@94.124.161.80:50101",
    "lantaogg:ejUXvrHFmW@50.114.107.110:50101",
    "lantaogg:ejUXvrHFmW@95.164.150.122:50101",
    "lantaogg:ejUXvrHFmW@50.114.106.18:50101",
    "lantaogg:ejUXvrHFmW@185.68.245.160:50101",
    "lantaogg:ejUXvrHFmW@185.240.120.137:50101",
    "lantaogg:ejUXvrHFmW@74.80.255.5:50101",
    "lantaogg:ejUXvrHFmW@199.181.239.29:50101",
    "lantaogg:ejUXvrHFmW@50.114.85.125:50101",
    "lantaogg:ejUXvrHFmW@216.185.46.172:50101",
    "lantaogg:ejUXvrHFmW@199.181.239.247:50101",
    "lantaogg:ejUXvrHFmW@194.5.148.12:50101",
    "lantaogg:ejUXvrHFmW@181.215.185.48:50101",
    "lantaogg:ejUXvrHFmW@64.113.1.228:50101",
    "lantaogg:ejUXvrHFmW@192.101.66.127:50101",
    "lantaogg:ejUXvrHFmW@74.80.255.185:50101",
    "lantaogg:ejUXvrHFmW@63.223.67.136:50101",
    "lantaogg:ejUXvrHFmW@95.164.145.173:50101",
    "lantaogg:ejUXvrHFmW@194.233.150.183:50101",
    "lantaogg:ejUXvrHFmW@94.131.86.114:50101",
    "lantaogg:ejUXvrHFmW@193.169.218.201:50101",
    "lantaogg:ejUXvrHFmW@95.164.151.8:50101",
    "lantaogg:ejUXvrHFmW@74.80.255.12:50101",
    "lantaogg:ejUXvrHFmW@213.170.223.39:50101",
    "lantaogg:ejUXvrHFmW@94.124.160.119:50101",
    "lantaogg:ejUXvrHFmW@185.240.121.66:50101",
    "lantaogg:ejUXvrHFmW@185.240.121.114:50101",
    "lantaogg:ejUXvrHFmW@194.233.150.136:50101",
    "lantaogg:ejUXvrHFmW@194.233.150.41:50101",
    "lantaogg:ejUXvrHFmW@194.233.150.67:50101",
    "lantaogg:ejUXvrHFmW@86.38.130.166:50101",
    "lantaogg:ejUXvrHFmW@86.38.130.55:50101",
    "lantaogg:ejUXvrHFmW@89.116.172.54:50101",
    "lantaogg:ejUXvrHFmW@89.116.172.101:50101",
    "lantaogg:ejUXvrHFmW@89.116.172.33:50101",
    "lantaogg:ejUXvrHFmW@89.116.172.121:50101",
    "lantaogg:ejUXvrHFmW@89.116.172.49:50101",
    "lantaogg:ejUXvrHFmW@89.116.172.59:50101"
]

# 连接到 Redis 数据库 9
redis_client = redis.StrictRedis(host='localhost', port=6379, password='Aa987987.',db=8)


# 将代理信息存储到 Redis 集合中
for proxy in proxies:
    proxy_info = proxy.split("@")
    auth_info, proxy_ip_port = proxy_info[0], proxy_info[1]
    username, password = auth_info.split(":")
    proxy_ip, proxy_port = proxy_ip_port.split(":")

    proxies = f"socks5://{username}:{password}@{proxy_ip}:{proxy_port}"
    redis_client.sadd("proxy:ips", proxies)

print("代理信息已成功存储到 Redis 数据库 9")
