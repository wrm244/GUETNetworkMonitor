import requests
import os
def check_internet_connection():
    try:
        # 从系统环境变量中获取代理设置
        http_proxy = os.environ.get('HTTP_PROXY')
        https_proxy = os.environ.get('HTTPS_PROXY')
        # 构造代理字典
        proxies = {
            'http': http_proxy,
            'https': https_proxy,
        }
        response = requests.get("https://www.baidu.com", timeout=5 ,proxies=proxies)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False
print(check_internet_connection())