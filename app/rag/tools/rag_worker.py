import weaviate
from langchain_openai import OpenAIEmbeddings
from langchain_weaviate.vectorstores import WeaviateVectorStore
from dotenv import load_dotenv
from ..util.rag_util import load_config
from ..util.loader import import_data

# Class to interface with embeddings and weaviate to load docs
class RagWorker():

    def __init__(self, weaviate_client, embeddings):

        # Load config
        self.config = load_config()    
        self.weaviate_client = weaviate_client
        self.embeddings = embeddings  
        file_path = f"./data/{self.config["filename"]}"

        print("Importing data")
        self.docs = import_data(self.config['source_urls'] , file_path)  
        self.load_wv_docs(self.docs)
        print("Rag_worker initialized")

    def get_docs(self):
        return self.docs 
    
    # Load Weaviate docs
    def load_wv_docs(self, docs) -> WeaviateVectorStore:
        self.db = WeaviateVectorStore.from_documents(docs, 
                                            self.embeddings, 
                                            client=self.weaviate_client, 
                                            tenant=self.config["tenant"],
                                            )
        return self.db

    # Load Weaviate texts                    
    def load_wv_texts(self, texts) -> WeaviateVectorStore:
        self.db = WeaviateVectorStore.from_texts(texts, 
                                            self.embeddings, 
                                            client=self.weaviate_client, 
                                            metadatas=[{"source": f"{i}-pl"} for i in range(len(texts))],
                                            )
        return self.db

    # Perform basic similarity search    
    def similarity_search(self, query):
        docs = self.db.similarity_search(query, 
                                         tenant=self.config["tenant"])
        return docs
    
    # Perform similarity search with filter and scoring
    def similarity_search_with_score(self, filter, k=5):
        docs = self.db.similarity_search_with_score(filter, 
                                                    k, 
                                                    tenant=self.config["tenant"])
        return docs