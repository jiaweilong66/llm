# -*- coding: utf-8 -*-
# ----------------------------
# @Time    : 2024/5/1 20:56
# @Author  : acedar
# @FileName: ali_api_verify.py
# ----------------------------
import os
from http import HTTPStatus
import dashscope

api_key = os.environ.get("ALI_API_KEY")

def call_with_messages():
    messages = [
        {'role': 'system', 'content': '你是一个时间管理大师'},
        {'role': 'user', 'content': '如何高效的安排时间'}]
    response = dashscope.Generation.call(
        'qwen1.5-110b-chat',
        messages=messages,
        api_key=api_key,
        result_format='message',  # set the result is message format.
    )
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))


if __name__ == '__main__':
    call_with_messages()
