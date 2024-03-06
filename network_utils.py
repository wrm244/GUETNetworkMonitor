# network_utils.py

import subprocess
import socket
import socket
import struct, os, re


def get_physical_mac_address():
    try:
        # Windows
        result = subprocess.run(['getmac'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if '物理地址' in line:
                    index = lines.index(line)
                    mac_address_line = lines[index + 2]
                    mac_address = mac_address_line.split()[0]
                    return mac_address.replace('-', '')
    except FileNotFoundError:
        pass

    try:
        # macOS or Linux
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'ether' in line:
                    return line.split()[1]
    except FileNotFoundError:
        pass

    return None


def get_network_info():
    try:
        wlan_user_ip = get_ip()
        wlan_ac_ip = socket.gethostbyname('')
        wlan_user_mac = get_physical_mac_address()
        return wlan_user_ip, wlan_ac_ip, wlan_user_mac
    except Exception as e:
        print("获取网络信息失败:", e)
        return None, None, None


def get_ip():  # 更准确获取IP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def ip_to_int(ip):
    try:
        return struct.unpack("!I", socket.inet_aton(ip))[0]
    except Exception as e:
        print("IP地址转换失败:", e)
        return None


def validate_ip(ip):
    # 使用正则表达式验证IP地址格式
    ip_regex = r'10(?:(?:\.1[0-9][0-9])|(?:\.2[0-4][0-9])|(?:\.25[0-5])|(?:\.[1-9][0-9])|(?:\.[0-9])){3}'
    return re.match(ip_regex, ip) is not None


def validate_mac(mac):
    # 删除mac地址中的冒号或破折号
    mac = mac.replace(':', '').replace('-', '').replace(" ", "")
    # 使用正则表达式验证MAC地址格式
    mac_regex = r'^([0-9A-Fa-f]{12})$'
    return re.match(mac_regex, mac) is not None


def format_mac(mac):
    # 删除mac地址中的冒号或破折号，然后转换为大写字母形式
    return mac.replace(':', '').replace('-', '').replace(" ", "").upper()
