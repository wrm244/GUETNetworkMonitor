import os,requests
def check_internet_connection():
    try:
        # 从系统环境变量中获取代理设置(你开了代理我也不怕)
        http_proxy = os.environ.get('HTTP_PROXY') 
        https_proxy = os.environ.get('HTTPS_PROXY')
        # 构造代理字典
        proxies = {
            'http': http_proxy,
            'https': https_proxy,
        }
        response = requests.get("https://www.baidu.com", timeout=5 ,proxies=proxies, verify=False,headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41"})
        print(response)
        if response.status_code == 200:
            return 1
        else:
            return 2
    except Exception as e:
        return e

print(check_internet_connection())