# authentication_utils.py

import json

import requests

from encryption_utils import base64_encrypt
from network_utils import get_network_info, ip_to_int, format_mac


def login(url, user_account, user_password, user_operators=''):
    try:
        wlan_user_ip, wlan_ac_ip, wlan_user_mac = get_network_info()
        if None not in (wlan_user_ip, wlan_ac_ip, wlan_user_mac):
            encrypted_password = base64_encrypt(user_password)
            if encrypted_password:
                login_params = {
                    'callback': 'dr1003',
                    'login_method': '1',
                    'user_account': f',0,{user_account}@{user_operators}',
                    'user_password': encrypted_password,
                    'wlan_user_ip': wlan_user_ip,
                    'wlan_user_ipv6': '',
                    'wlan_user_mac': wlan_user_mac,
                    'wlan_ac_ip': wlan_ac_ip,
                    'wlan_ac_name': 'HJ-BRAS-ME60-01'
                }
                response = requests.get(url, params=login_params)
                if response.status_code == 200:
                    result = json.loads(response.text[7:-2])
                    if result['result'] == 1:
                        return {1, result['msg']}
                    elif result['result'] == 0:
                        result_msg = result['msg']
                        if "已经在线" in result_msg:
                            return {2, result['msg']}
                        elif "1.2.3.4" in result_msg:
                            return {3, result[
                                'msg']}  # "登录失败,请查看：wlan_ip: "+wlan_user_ip +" mac: "+wlan_user_mac + " 是否正确"
                        else:
                            return "登录失败 " + result['msg']
                    else:
                        return "登录失败, 未知原因。"
                else:
                    return "登录失败。是否连接到校园网?或者重新点击按钮。"
        else:
            return "获取网络信息失败，请重启软件"
    except Exception as e:
        return "登录失败"


def login_unmac(url, user_account, user_password, wlan_user_ip, wlan_user_mac, user_operators=''):
    try:
        encrypted_password = base64_encrypt(user_password)
        if encrypted_password:
            login_params = {
                'callback': 'dr1003',
                'login_method': '1',
                'user_account': f',0,{user_account}@{user_operators}',
                'user_password': encrypted_password,
                'wlan_user_ip': wlan_user_ip,
                'wlan_user_ipv6': '',
                'wlan_user_mac': wlan_user_mac,
                'wlan_ac_ip': '',
                'wlan_ac_name': 'HJ-BRAS-ME60-01'
            }
            response = requests.get(url, params=login_params)
            if response.status_code == 200:
                result = json.loads(response.text[7:-2])
                if result['result'] == 1:
                    return {1, result['msg']}
                elif result['result'] == 0:
                    result_msg = result['msg']
                    if "已经在线" in result_msg:
                        return {2, result['msg']}
                    elif "1.2.3.4" in result_msg:
                        return {3, result['msg']}  # "登录失败,请查看：wlan_ip: "+wlan_user_ip +" mac: "+wlan_user_mac + " 是否正确"
                    else:
                        return "登录失败 " + result['msg']
                else:
                    return "登录失败, 未知原因。"
            else:
                return "登录失败。是否连接到校园网?或者重新点击按钮。"
    except Exception as e:
        return "登录失败"


def logout(url, username):
    try:
        wlan_user_ip, _, wlan_user_mac = get_network_info()
        if None not in (wlan_user_ip, wlan_user_mac):
            wlan_user_ip = ip_to_int(wlan_user_ip)
            wlan_user_mac = format_mac(wlan_user_mac)
            if wlan_user_ip and wlan_user_mac:
                logout_params = {
                    'callback': 'dr1002',
                    'user_account': f'{username}',
                    'wlan_user_mac': wlan_user_mac,
                    'wlan_user_ip': wlan_user_ip
                }
                response = requests.get(url, params=logout_params)
                result = json.loads(response.text[7:-2])
                if response.status_code == 200:
                    return result['msg']
        else:
            return "获取网络信息失败。"
    except Exception as e:
        print("注销失败:", e)
