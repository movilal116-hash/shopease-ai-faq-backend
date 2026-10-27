# import 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings
import os

from langchain_chroma import Chroma
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS

# SetUp jina ai
from langchain_community.embeddings import JinaEmbeddings

# DocumentLoader
loader = PyPDFLoader("shopease_faq.pdf")
docs = loader.load()


# Split into chunks and
from langchain_text_splitters import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size = 600,
    chunk_overlap=100
)

chunks = splitter.split_documents(docs)

# convert (Embedding) vectors

load_dotenv()

# This committed code download the model that creates the problem during deploying in render # without deployee free this is best 
# embeddings = HuggingFaceEmbeddings(
#     model_name="sentence-transformers/all-MiniLM-L6-v2",
#     encode_kwargs={"normalize_embeddings":True}

# )

# without download using api key
# embeddings = HuggingFaceEndpointEmbeddings(
#     model="sentence-transformers/all-MiniLM-L6-v2"
# )


# Without Download using jina api key
embeddings = JinaEmbeddings(
    api_key=os.getenv("JINA_API_KEY"),
    model_name="jina-embeddings-v2-base-en"
)


##################################### vector Store with Chroma
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./Chroma_db"
    )

# data = vector_store._collection.get(include=["documents", "metadatas"])
# for idx, doc in enumerate(data["ids"]):
#     print(f"{idx + 1}: {doc}")

#                         Or

######################################## vector Store with FAISS
# vector_store = FAISS.from_documents(chunks, embeddings)
# print(vector_store.index_to_docstore_id)



######################################### Retrival
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3}) #### as a list 3 similar vectors
# retriever
# retriever.invoke("How do I place an order ?")


# Augmentation and Generation 

prompt = PromptTemplate(
    template="""
You are a helpful assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:
""",
input_variables=["context", "question"]
)
question = "Can I place a bulk or corporate order?"
# question = "Do you sell laptops?"

llm = ChatGroq(
    api_key=os.getenv("api_key"),
    model="openai/gpt-oss-120b",
    temperature=0.0

)
retriever_docs = retriever.invoke(question) ##  retrieves only required or related docs

res = llm.invoke(prompt.format(context=retriever_docs, question=question))
print(">> ")

print(res.content)
