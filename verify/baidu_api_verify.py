# -*- encoding: utf-8 -*-
"""
@author: acedar  
@time: 2024/3/31 13:38
@file: baidu_api_verify.py 
"""

import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("BAIDU_API_KEY")
SECRET_KEY = os.environ.get("BAIDU_SECRET_KEY")


def main():
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/yi_34b_chat?access_token=" + get_access_token()

    request_data = {
        "messages": [
            {"role": "user", "content": "如何保持好的睡眠？"}
        ],
        "top_p": 0.9,
        "temperature": 0.1,
        "stream": False
    }
    payload = json.dumps(request_data)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.json()['result'])
    # print(response.text)


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    main()
