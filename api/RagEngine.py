import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import JinaEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings  ##### add this can be deployed on render
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

class RAGEngine:
    def __init__(self):
        loader = PyPDFLoader("shopease_faq.pdf")
        docs = loader.load()
        print(f"SUCCESS: Loaded {len(docs)} pages from the PDF!")

        splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        
        # embeddings = JinaEmbeddings(
        #     api_key=os.getenv("JINA_API_KEY"),
        #     model_name="jina-embeddings-v2-base-en"
        # )

            # for easy to deployed so use this end-point
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001", # Current free-tier embedding model
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        
        vector_store = Chroma.from_documents(chunks, embeddings)
        self.retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        
        self.llm = ChatGroq(
            api_key=os.getenv("api_key"),
            model="openai/gpt-oss-120b",
            temperature=0.0
        )
        
        self.prompt = PromptTemplate(
            template="""
You are a helpful assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:
""",
            input_variables=["context", "question"]
        )

    def get_answer(self, question: str) -> str:
        retriever_docs = self.retriever.invoke(question)
        res = self.llm.invoke(self.prompt.format(context=retriever_docs, question=question))
        return res.content

rag_engine = RAGEngine()