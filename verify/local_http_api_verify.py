# -*- coding: utf-8 -*-
# ----------------------------
# @Time    : 2024/4/6 10:35
# @Author  : acedar
# @FileName: local_http_api_verify.py
# ----------------------------

import os
import requests
import json

url_root = os.environ.get("URL_ROOT", 'http://127.0.0.1:8000')

def health():
    url = os.path.join(url_root, 'health')
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request('GET', url, headers=headers)
    print('status:', response.status_code)
    assert response.status_code == 200

def main():
    url = os.path.join(url_root, 'v1/chat/completions')
    headers = {
        'Content-Type': 'application/json'
    }
    payload = json.dumps({
        'messages': [
            {
                'role': 'user',
                'content': '如何理财？'
            }
        ],
        'temperature': 0.1,
        'top_p': 0.9,
        'max_tokens': 1024,
        'stream': False,
        'model': 'chatglm3-6b'
    })
    response = requests.request('POST', url, headers=headers, data=payload)
    print('json:', response.json())
    return response.json()


if __name__ == "__main__":
    health()
    json_res = main()
    print('json_res:', json_res['result'])


