from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
from langchain_core.prompts import PromptTemplate
import os

# 1️⃣ Load PDF
loader = TextLoader("wryd_wiki.txt", encoding="utf-8")
documents = loader.load()

# 2️⃣ Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
docs = text_splitter.split_documents(documents)

# 3️⃣ Create embeddings (local)
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 4️⃣ Store in ChromaDB (persistent)
persist_directory = "./chroma_db"

if os.path.exists(persist_directory):
    print("Loading existing Chroma DB...")
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
else:
    print("Creating new Chroma DB...")
    vectorstore = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=persist_directory
    )

    
# 6️⃣ SYSTEM PROMPT + HUMAN PROMPT
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful AI assistant wryd
Answer ONLY using the provided context.

Context:
{context}

Question:
{question}

Answer:
"""
)

# 5️⃣ Load LLM (local)
llm = ChatOllama(
    model="llama3:latest",
    temperature=0.5
    )

# 6️⃣ Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=True
)

# 7️⃣ Ask question
def ask_llm(query):
    response = qa_chain.invoke({"query":query})
    return response["result"]























































