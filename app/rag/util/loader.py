
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents.base import Document


import os
from .rag_util import donwload_article

# Import a list 
def import_data(source_urls, file_path) -> list[Document]:
    try:    
        # Download the articles to our source file
        if not os.path.exists(file_path):
            donwload_article(source_urls, file_path)

        # Load our source file and generate documents
        loader = TextLoader(file_path)
        documents = loader.load()
        #text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        # Using recursive character text splitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        return docs

    except Exception as e:
            print(f"An error occurred during the request: {e}")
            # Handle network errors, connection issues, etc.
            exit() # Or handle the error appropriately
