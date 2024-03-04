## 桂电校园网断线重连 (GUETNetworkMonitor) <img src="https://github.com/wrm244/GUETNetworkMonitor/assets/54385511/a75aef06-35dd-42ad-8353-7a98b10e4ba7" width="90" height="90" align="right">

> 该应用采用pyQt5设计交互，这边只打包了windows可执行文件，可在Action处下载，也可以在Releases中下载

### 请求逻辑

> guet的登录逻辑比之前安全些，同时也加了密，采用的是JS后台GET请求，虽然说之前是直接在浏览器地址框直接请求，但也安全多。

```python
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
```

### 界面

界面简洁，在登录后会出现监视日志窗口，每15秒测试互联网连接，如果连不上就重新登录账号，实现自动化断网重连

> PS:适合运行在实验室的一台主机上(当然源码可以编译linux可执行文件，请你尝试，同时还有简易脚本``linux.py``文件中)
> 可以尝试连接在路由器的实验室主机，同时登录有宽带的账号，岂不美哉

<p align=center>
<img alt="登录界面" width="150" src="https://github.com/wrm244/GUETNetworkMonitor/assets/54385511/f2c1fefd-9803-4027-9b14-9dc10ed7a6ae" />

<img alt="提示" width="150" src="https://github.com/wrm244/GUETNetworkMonitor/assets/54385511/4d149074-5024-49ca-ab21-f26db6f4b4f2" />

<img alt="日志窗口" width="300" src="https://github.com/wrm244/GUETNetworkMonitor/assets/54385511/e00ea5fb-c52b-4762-b3e2-6231cc51b394" />

</p>

![image](https://github.com/wrm244/GUETNetworkMonitor/assets/54385511/e592ab29-a0f4-4f88-888a-6acda8235608)

### 特性
- [x] 一键登录
- [x] 自动化监管网络，不怕账号挤出
- [ ] 未来实现流量数据统计，细枝末节，注意限速新规定 
