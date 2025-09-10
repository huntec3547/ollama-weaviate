from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from .rag_worker import RagWorker
from dotenv import load_dotenv

# Class to handle weaviate search and LLM chain
class RagChain():
    
    def __init__(self, rag_worker):
        self.rag_worker = rag_worker
        #Convert our docs to text for weaviate search
        texts = []
        for doc in self.rag_worker.get_docs():
            texts.append(doc.page_content)
        self.docsearch = self.rag_worker.load_wv_texts(texts)

    # Invoke our Chain with prompt(question,context), llm, and wv retriever
    def invoke(self, question, context):
        retriever = self.docsearch.as_retriever()

        template = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
        Question: {question}
        Context: {context}
        Answer:
        """
        prompt = ChatPromptTemplate.from_template(template)

        print(prompt)

        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return chain.invoke(question)