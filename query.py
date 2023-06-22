from llama_index import StorageContext,load_index_from_storage
import openai
import os
import streamlit as st

try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except:
    pass

def generate_response(prompt):
    storage_context = StorageContext.from_defaults(persist_dir="index")

    # Load the previously saved index
    index = load_index_from_storage(storage_context=storage_context)

    # Make a query engine
    query_engine = index.as_query_engine()

    response = query_engine.query(prompt)
    return str(response)




if __name__ == "__main__":
    prompt = "Does he has experience in Gensim"
    generate_response(prompt)
