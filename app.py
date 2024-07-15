from llama_index.llms.groq import Groq
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
import gradio as gr 
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
# llm = Groq(model="gemma2-9b-it",api_key=API_KEY)


def greet(name:str, intensity:int):
    return "Hello, " + name + "!" * intensity

single_stock = gr.Interface(fn=greet, 
                    inputs=["text", "slider"],
                    outputs=["text"],
                    title="Single stock report")


compete_stock = gr.Interface(fn=greet, 
                    inputs=["text", "slider"],
                    outputs=["text"],
                    title="Between two stocks")


demo = gr.TabbedInterface([single_stock, compete_stock],["Single", "Compete"])

demo.launch()

