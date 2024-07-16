from llama_index.llms.groq import Groq
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import CitationQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import gradio as gr 
from utils.news import save_all_articles
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
llm = Groq(model="gemma2-9b-it",api_key=API_KEY)
llm.max_tokens
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
llm.system_prompt = "You are sebi registered financial expert. You have to help people invest better. You only reply in markdown well formatted text that looks pretty."




def individual_handler(Symbol:str):
    if not os.path.exists(f"data/{Symbol.lower()}/"):
        save_all_articles(Symbol.upper(), directory=f"data/{Symbol.lower()}/")
    documents = SimpleDirectoryReader(f"data/{Symbol.lower()}/").load_data()
    index = VectorStoreIndex.from_documents(documents)
    retr = VectorIndexRetriever(index=index, similarity_top_k=7)
    query_engine = CitationQueryEngine(retr, llm=llm)
    response = query_engine.query(f"Write a report on the outlook for {Symbol} stock from the years 2024-2027. Be sure to include potential risks and headwinds in bulleted points.")
    return str(response)

def competitor_handler(Symbol_1:str, Symbol_2:str):
    if not os.path.exists(f"data/{Symbol_1.lower()}/"):
            save_all_articles(Symbol_1.upper(), directory=f"data/{Symbol_1.lower()}/")
    if not os.path.exists(f"data/{Symbol_2.lower()}/"):
            save_all_articles(Symbol_2.upper(), directory=f"data/{Symbol_2.lower()}/")


    documents_1 = SimpleDirectoryReader(f"data/{Symbol_1.lower()}/").load_data()
    documents_2 = SimpleDirectoryReader(f"data/{Symbol_2.lower()}/").load_data()
    documents_1.extend(documents_2)


    index = VectorStoreIndex.from_documents(documents=documents_1)
    retr = VectorIndexRetriever(index=index)
    query_engine = CitationQueryEngine(retr, llm=llm)
    response = query_engine.query(f"You are given recent news trends for {Symbol_1} and {Symbol_2} you have to write a report on their future performance vs each other. Point out few important trends from context. List out bullet points for each")
    return str(response)





individual_stock = gr.Interface(fn=individual_handler, 
                    inputs=["text"],
                    outputs=gr.Markdown(),
                    title="Individual stock report")


competitor_stock_outlook = gr.Interface(fn=competitor_handler, 
                    inputs=["text", "text"],
                    outputs=gr.Markdown(),
                    title="Competitor outlook",
                    description="Provide symbols of two stocks you want report for ")


demo = gr.TabbedInterface([individual_stock, competitor_stock_outlook],["Individual Stock Report", "Competitor outlook"])

demo.launch()

