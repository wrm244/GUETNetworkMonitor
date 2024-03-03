# network_utils.py

import subprocess
import socket
import socket
import struct

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
        wlan_user_ip = socket.gethostbyname(socket.gethostname())
        wlan_ac_ip = socket.gethostbyname('')
        wlan_user_mac = get_physical_mac_address()
        return wlan_user_ip, wlan_ac_ip, wlan_user_mac
    except Exception as e:
        print("获取网络信息失败:", e)
        return None, None, None
    
def ip_to_int(ip):
    try:
        return struct.unpack("!I", socket.inet_aton(ip))[0]
    except Exception as e:
        print("IP地址转换失败:", e)
        return None

def format_mac(mac_address):
    try:
        return mac_address.upper().replace(':', '')
    except Exception as e:
        print("MAC地址格式化失败:", e)
        return None