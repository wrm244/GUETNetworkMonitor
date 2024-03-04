import os
import json
import base64
import requests
import urllib3

urllib3.disable_warnings()
def save_encrypted_login_info(username, password, operator):
    login_info = {
        'username': base64.b64encode(username.encode()).decode(),
        'password': base64.b64encode(password.encode()).decode(),
        'operator': base64.b64encode(operator.encode()).decode()
    }
    with open('login_info.json', 'w') as f:
        json.dump(login_info, f)

def load_decrypted_login_info():
    try:
        with open('login_info.json', 'r') as f:
            login_info = json.load(f)
            return base64.b64decode(login_info['username']).decode(), base64.b64decode(login_info['password']).decode(), base64.b64decode(login_info['operator']).decode()
    except FileNotFoundError:
        return None, None, None

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
        response = requests.get("https://www.baidu.com", timeout=5 ,proxies=proxies, verify=False)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False
