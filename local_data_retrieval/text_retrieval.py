# -*- encoding: utf-8 -*-
"""
@author: acedar  
@time: 2024/3/31 14:37
@file: text_retrieval.py
"""

import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders.json_loader import JSONLoader

from langchain.vectorstores import Chroma

embed_model_map = {
    "text2vec-base": "E:\\py_workspace\\models\\text2vec-base-chinese",
}

class Text2embedStore(object):

    def __init__(self, model_name):
        self.model_name = model_name
        file_path = os.environ.get("FILE_PATH")

        self.text_split = None
        self.text_split_init()
        self.embed_model_init()
        if file_path:
            self.load_dir(file_path)

    def text_split_init(self):
        text_split_name = os.environ.get("TEXT_SPLIT_METHOD")
        chunk_size = int(os.environ.get("CHUNK_SIZE", 256))
        chunk_overlap = int(os.environ.get("CHUNK_OVERLAP", 128))
        if text_split_name == 'char':
            self.text_split = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        else:
            self.text_split = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    def embed_model_init(self):
        persist_directory = os.environ.get("PERSIST_DIRECTORT", './data/vector_store')
        self.embed_model = self.load_embedding_model(self.model_name)

        db_name = os.environ.get("VECTOR_DB_NAME", 'chroma')
        if db_name == 'chroma':
            self.db = Chroma(persist_directory=persist_directory, embedding_function=self.embed_model)
        else:
            self.db = Chroma(persist_directory=persist_directory, embedding_function=self.embed_model)


    def load_embedding_model(self, model_name):

        if model_name not in embed_model_map:
            raise ValueError("embed model not set right, you can select from {}".format(list(embed_model_map.keys())))
        embed_model = HuggingFaceEmbeddings(model_name=embed_model_map[model_name])
        return embed_model

    def load_dir(self, file_path):
        if os.path.isdir(file_path):
            for root, ds, fs in os.walk(file_path):
                for f in fs:
                    self.load_file(file_name=f)
        else:
            self.load_file(file_path)

    def load_file(self, file_name):
        print("file_name", file_name)
        if file_name.endswith('.pdf') or file_name.endswith('.PDF'):
            loader = PyPDFLoader(file_name)
        elif file_name.endswith('.csv') or file_name.endswith('.CSV'):
            loader = CSVLoader(file_name)
        elif file_name.endswith('.json'):
            # [{"text": ...}, {"text": ...}, {"text": ...}] -> schema =.[].text
            # {"key": [{"text": ...}, {"text": ...}, {"text": ...}]} -> schema =.key[].text
            # ["", "", ""] -> schema =.[]
            # todo: 提前读取json文件，解析schema
            loader = JSONLoader(file_name, '.key[].text')
        else:
            raise ValueError('not support this type file, {}, you can upload file type: {}'.format(
                file_name, ['pdf', 'csv', 'json']))

        documents = loader.load()
        docs = self.text_split.split_documents(documents)
        if docs:
            self.db.add_documents(docs)

    def as_retriever(self):
        return self.db.as_retriever()

    def as_db(self):
        return self.db
