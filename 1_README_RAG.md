# Dependencies, libraries and  packages
 pip install langchain-community langchain-groq python-dotenv pypdf langchain-text-splitters langchain-huggingface sentence-transformers langchain-chroma faiss-cpu langchain-groq



# import 
 from langchain_community.document_loaders import PyPDFLoader
 from langchain_text_splitters import RecursiveCharacterTextSplitter
 from langchain_huggingface import HuggingFaceEmbeddings
 import os
 from langchain_chroma import Chroma
 from dotenv import load_dotenv

 from langchain_core.prompts import PromptTemplate
 from langchain_groq import ChatGroq

 from langchain_chroma import Chroma
 from langchain_community.vectorstores import FAISS


# DocumentLoader

# TextSplit into chunks

# Chunks converted into Embedded for Semantic Search

# Vector Store
# 

Flow of the Project -> RAG_Based_FAQ_Chatbot
Document and prepare content

Split into chunks

Chunks convert into Vector (Embedding)

Retrieval (context) based on question only important part

Augmented (context + Question) -> prompt

Generate response that will show to the client or users

UI with Streamlit
Attached a front-end to show
Deploye on render.com and AWS
Add portfolio
Project Flow: RAG-Based FAQ Chatbot
Phase 1: Data Ingestion & Preparation
Load Documents: Import the business's FAQ text/PDF files.
Text Splitting: Break the large document into smaller, semantically meaningful chunks to ensure the LLM can process them efficiently.
Phase 2: Embedding & Storage
Generate Embeddings: Convert the text chunks into numerical vectors (dense arrays) using an embedding model.

Vector Store: Store these vectors in a local vector database (like FAISS or Chroma) for fast and efficient searching.

Phase 3: Retrieval & Augmentation (The RAG Core)
Retrieval: When a user asks a question, convert the question into a vector and search the database to retrieve only the most relevant context.
Augmentation: Combine the retrieved context with the user's question into a strict Prompt Template.
Phase 4: Generation
LLM Response: Pass the augmented prompt to the LLM. The LLM generates a safe, accurate response based only on the provided context (and politely says "I don't know" if the answer isn't there).
Display: Show the final answer to the customer.
Phase 5: Deployment & Portfolio (Freelancing Ready)
Build the UI: Create a clean, interactive front-end interface using Streamlit or Chainlit.

Deploy: Host the application live on the web using Render.com (free/easy) or AWS (industry standard).

Portfolio: Add the live link and a GitHub repository to your freelancing portfolio/resume to attract clients.

Summary
"I read your business PDF"
"I organize your data so the AI can find it instantly"
"When a customer asks a question, the AI searches your PDF, reads the exact answer, and replies to the customer safely."