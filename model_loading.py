import os
from dotenv import load_dotenv
from vanna.base import VannaBase
from vanna.chromadb import ChromaDB_VectorStore
from langchain_openai import ChatOpenAI
import streamlit as st

load_dotenv()
os.environ['OPENAI_API_KEY']=st.secrets["OPENAI_API_KEY"]
## langsmit Tracking
os.environ['LANGCHAIN_API_KEY']=st.secrets["LANGCHAIN_API_KEY"]
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANGCHAIN_PROJECT']=st.secrets["LANGCHAIN_PROJECT"]


class MyCustomLLM(VannaBase):
    def __init__(self, config=None):
        VannaBase.__init__(self, config=config)

        self.temperature = 0.7
        self.client = ChatOpenAI(model="gpt-4o")

    def system_message(self, message: str) -> any:
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> any:
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> any:
        return {"role": "assistant", "content": message}
    
    def submit_prompt(self, prompt, **kwargs) -> str:
        if prompt is None:
            raise Exception("Prompt is None")

        if len(prompt) == 0:
            raise Exception("Prompt is empty")
        
        else:
            response = self.client.invoke(
                input=prompt,
                stop=None,
                temperature=self.temperature,
            )
            

        # If no response with text is found, return the first response's content (which may be empty)
        return response.content
    

class MyVanna(ChromaDB_VectorStore, MyCustomLLM):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        MyCustomLLM.__init__(self, config=config)
