import os
import time
from http.client import responses

import gradio as gr
from dotenv import load_dotenv

load_dotenv()
rag =RAG()
def add_text(history, text):
    print("add_text")
    history = history + [[text, None]]
    return  history,gr.update(value='',interactive=False)

def upload_file(history, file):
    print("upload file")
    """
    1.上传文档
    2.文档切割
    3.文档向量化
    4.检索
    """
    rag.load_dir(file.name)
    history = history + [((file.name, ),None)]
    return history
def chat(history):
    print("chat")
    msg =history[-1][0]
    if isinstance(msg,tuple):
        ans='文件上传成功！'
    else:

        """
        #todo:
        1.根据用户提问，检索
        2.调用大模型进行整合
        3.解析大模型结果并返回
        """
        responses=rag.retrival_qa()
        ans=''
        try:
            ans=responses['result']
            # ans='待调用大模型,敬请期待'
        except Exception as err:
            print("err:{},ans:{}".format(err,responses))

    history[-1][1]=''
    for ch in ans:
        history[-1][1] += ch
        time.sleep(0.01)
        yield history[-1:]

with gr.Blocks() as demo:
    with gr.Tab("RAG文本对话"):
        model_list=["百度零-34b大模型","chatglm3"]
        input_model_list=gr.Dropdown(choices=model_list,label="模型选择")

        chatbot = gr.Chatbot(
        [],
        elem_id='chatbot',
        bubble_full_width=False,
    )
        with gr.Row():
            txt =gr.Textbox(
                scale=4,
                show_label=False,
                placeholder="请输入问题并回车,后者上传本地文件",
                container=False
            )
            btn = gr.UploadButton("文件", file_types=[])

        txt_msg = txt.submit(add_text,[chatbot,txt],[chatbot,txt], queue=False).then(
            chat,chatbot,chatbot
        )
        file_msg = btn.upload(upload_file,[chatbot,btn],[chatbot], queue=False).then(
            chat,chatbot,chatbot
        )

demo.queue()

if __name__ == "__main__":
    demo.launch()