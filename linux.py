import time
import os
import requests
import logging
import threading
from authentication_utils import login, logout
import urllib3

urllib3.disable_warnings()
# 设置日志
logging.basicConfig(filename='network_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')
lock = threading.Lock()


def perform_request(login_url, username, password, operator_code):
    try:
        # 从系统环境变量中获取代理设置(你开了代理我也不怕)
        http_proxy = os.environ.get('HTTP_PROXY')
        https_proxy = os.environ.get('HTTPS_PROXY')
        # 构造代理字典
        proxies = {
            'http': http_proxy,
            'https': https_proxy,
        }
        while True:
            try:
                # 每10秒发送一次GET请求到百度
                response = requests.get('https://www.baidu.com', timeout=5, verify=False, proxies=proxies)

                # 如果不是200，则重新登录并写入日志文件
                if response.status_code != 200:
                    with lock:
                        print('检测到网络不稳定，尝试重新登录')
                    login_result = login(login_url, username, password, operator_code)
                    if login_result == 1:
                        with lock:
                            print('登录成功')
                    elif login_result == 2:
                        with lock:
                            print('已经在线，正在监控')
                else:
                    with lock:
                        print('网络一切正常')
                time.sleep(10)
            except requests.Timeout:
                # 处理超时异常
                with lock:
                    print('请求超时，尝试重新登录')
                login_result = login(login_url, username, password, operator_code)
                if login_result == 1:
                    with lock:
                        print('登录成功')
                elif login_result == 2:
                    with lock:
                        print('已经在线，正在监控')
    except Exception as e:
        print("你有可能没连上wifi或者网线，请连上再次运行！")
        return False


if __name__ == "__main__":
    # 设置登录地址
    login_url = "http://10.0.1.5:801/eportal/portal/login"
    logout_url = "http://10.0.1.5:801/eportal/portal/mac/unbind"
    print("桂电校园网断网重连脚本版本(适用于Linux)，请按照提示输入，前台运行有能力的同学可以记录日志和挂后台")
    # 提示用户输入账号和密码
    username = input("请输入用户名: ")
    password = input("请输入密码: ")

    # 提示用户选择运营商
    print("请选择运营商：")
    print("1. 中国移动")
    print("2. 中国电信")
    print("3. 中国联通")
    print("4. 校园网")
    operator_choice = input("请输入选择的运营商编号（1/2/3/4）: ")

    # 将用户输入的运营商编号映射到运营商代码
    operator_code = ""
    if operator_choice == "1":
        operator_code = "cmcc"
    elif operator_choice == "2":
        operator_code = "telecom"
    elif operator_choice == "3":
        operator_code = "unicom"
    elif operator_choice == "4":
        operator_code = ""
    else:
        print("无效的选择")

    # 登录
    login_result = login(login_url, username, password, operator_code)
    if login_result == 1:
        print('登录成功')
    elif login_result == 2:
        print('已经在线，正在监控')
    else:
        print(login_result)

    # 创建线程执行请求
    request_thread = threading.Thread(target=perform_request, args=(login_url, username, password, operator_code))
    request_thread.start()
