from llama_index import VectorStoreIndex,GPTVectorStoreIndex,SimpleDirectoryReader
from llama_index import StorageContext,download_loader,load_index_from_storage
from dotenv import load_dotenv
from llama_index.node_parser import SimpleNodeParser
load_dotenv()
import openai
import os


# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# openai.api_key = OPENAI_API_KEY
openai.api_key = os.environ["OPENAI_API_KEY"]


def create_vector():
    # Check if index file already exists
    # if os.path.exists("index"):
    #     print("Index already exists. Skipping vector creation.")
    #     return

    # Create a loader
    if os.environ.get("OPENAI_API_KEY", "") != "":

         
        loader = SimpleDirectoryReader(input_dir="data")

        #1 Load the documents

        docs = loader.load_data()

        # 2. Parsing the documents
        parser = SimpleNodeParser()
        nodes = parser.get_nodes_from_documents(documents=docs)

        #3. Index construction This will create embeddings (check out this article for a visual explanation) for each node and store it in a Vector Store.

        index = GPTVectorStoreIndex(nodes=nodes)

        # 4. Store the index
        index.storage_context.persist(persist_dir="index")
        print("Vectors have been created.")

    else:
        print("Key eroor")
