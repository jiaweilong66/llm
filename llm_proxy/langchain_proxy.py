# -*- encoding: utf-8 -*-
"""
@author: acedar  
@time: 2024/3/31 14:21
@file: langchain_proxy.py 
"""

import os
# from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.llms.chatglm3 import ChatGLM3
from local_data_retrieval.text_retrieval import Text2embedStore
from llm_proxy.llm import BaiduLlm


qa_prompt = PromptTemplate.from_template("""
根据给出的上下文信息回答问题，如果从上下文信息中找不到答案就诚实的说不知道。
上下文信息: {context}
问题: {question}
""")


class RAG(object):

    def __init__(self):
        self.model_name = os.environ.get("MODEL_NAME")

        self.model_init()

    def model_init(self):
        # 向量相关的
        embed_model_name = os.environ.get("EMBED_MODEL_NAME")
        self.db = Text2embedStore(embed_model_name)

        if self.model_name == 'baidu-yi_34b_chat':
            model_name = self.model_name.replace('baidu-', '')
            llm = BaiduLlm(model_name=model_name)
        elif self.model_name == 'chatglm3':
            endpoint_url = os.environ.get('ENDPOINT_URL')
            max_tokens = int(os.environ.get("MAX_TOKENS", 1024))
            top_p = float(os.environ.get("TOP_P", 0.9))

            if not endpoint_url:
                raise ValueError('endpoint_url not right,url:{}'.format(endpoint_url))
            llm = ChatGLM3(
                endpoint_url=endpoint_url,
                max_tokens=max_tokens,
                top_p=top_p,
                prefix_messages=[]
            )
        else:
            raise ValueError("no llm to call")
        self.qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=self.db.as_retriever(),
            verbose=True,
            chain_type_kwargs={"prompt": qa_prompt}
        )

    def as_retrival_qa(self):
        return self.qa
