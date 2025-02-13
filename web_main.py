# -*- encoding: utf-8 -*-
"""
@author: acedar  
@time: 2024/3/31 13:52
@file: web_main.py 
"""

import os
import time
import gradio as gr
from dotenv import load_dotenv
from llm_proxy.langchain_proxy import RAG

load_dotenv()

rag = RAG()

def add_text(history, text):
    print("add_text")
    history = history + [(text, None)]
    return history, gr.update(value='', interactive=True)


def upload_file(history, file):
    print("upload file")
    """
        1. 上传文档
        2. 文档切割
        3. 文档向量化
        4. 检索
    """
    rag.db.load_dir(file.name)
    history = history + [((file.name, ), None)]
    print("upload_file,", history)
    return history


def chat(history):
    print("chat")
    print("upload_file,", history)

    msg = history[-1][0]
    if isinstance(msg, tuple):
        ans = '文件上传成功！'
    else:

        """
            # todo:
            1. 根据用户的提问，调用检索服务，获取与问题相关本地知识库信息
            2. 调用大模型，对信息进行整合
            3. 解析大模型结果，并返回
        """
        response = rag.as_retrival_qa()({"query": msg})
        ans = ''
        try:
            ans = response['result']
            # ans = '待调用检索服务及大模型，敬请期待'
        except Exception as err:
            print("err:{}, ans: {}".format(err, response))

    history[-1][1] = ''
    for ch in ans:
        history[-1][1] += ch
        time.sleep(0.01)
        yield history[-1:]


with gr.Blocks() as demo:
    with gr.Tab("RAG文本对话"):
        model_list = ["百度零一34b大模型", "chatglm3"]
        input_model_list = gr.Dropdown(choices=model_list, label='模型选择')

        chatbot = gr.Chatbot(
            [],
            elem_id='chatbot',
            bubble_full_width=False
        )

        with gr.Row():
            txt = gr.Textbox(
                scale=4,
                show_label=False,
                placeholder='输入文本并回车，后者上传本地文件',
                container=False
            )
            btn = gr.UploadButton("文件", file_types=[])

        txt_msg = txt.submit(add_text, [chatbot, txt], [chatbot, txt], queue=False).then(
            chat, chatbot, chatbot
        )
        file_msg = btn.upload(upload_file, [chatbot, btn], [chatbot], queue=False).then(
            chat, chatbot, chatbot
        )

demo.queue()

if __name__ == "__main__":
    demo.launch()


