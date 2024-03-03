# encryption_utils.py

import base64

def base64_encrypt(text):
    try:
        encrypted = base64.b64encode(text.encode()).decode()
        return encrypted
    except Exception as e:
        print("Base64加密失败:", e)
        return None
