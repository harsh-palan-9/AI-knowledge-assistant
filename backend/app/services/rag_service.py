import os
import time
from dotenv import load_dotenv

from groq import Groq

from pinecone import Pinecone

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from app.middleware.logging_middleware import document_logger, llm_logger


load_dotenv()

#Step 1: Embeddings (LangChain)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

#Step 2: Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX"))

#Step 3: Vector Store
vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

# Step 4: Retriever
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 10}
    )

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def call_llm(prompt: str):
    model = "llama-3.1-8b-instant"
    
    # Log LLM call start
    llm_logger.log_llm_call_start(prompt, model)
    
    start_time = time.time()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        
        response_time = time.time() - start_time
        response_content = response.choices[0].message.content
        response_length = len(response_content)
        
        # Log successful LLM call
        llm_logger.log_llm_call_complete(model, response_time, response_length)
        
        return response_content
        
    except Exception as e:
        response_time = time.time() - start_time
        # Log LLM call error
        llm_logger.log_llm_call_error(model, str(e))
        raise e

# 🔹 Prompt Template
prompt = ChatPromptTemplate.from_template("""
You are an AI assistant.

Answer ONLY using the context below.
If the answer is not present, say "I don't know".

Context:
{context}

Question:
{question}

Answer:
""")

# Format documents with logging
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# Enhanced retriever with logging
def retrieve_documents(query: str):
    """Retrieve documents with logging"""
    retrieval_params = {"search_type": "mmr", "k": 5, "fetch_k": 10}
    
    # Log retrieval start
    document_logger.log_retrieval_start(query, retrieval_params)
    
    start_time = time.time()
    try:
        docs = retriever.invoke(query)
        retrieval_time = time.time() - start_time
        
        # Log successful retrieval
        document_logger.log_retrieval_complete(query, docs, retrieval_time)
        
        return docs
        
    except Exception as e:
        retrieval_time = time.time() - start_time
        # Log retrieval error
        document_logger.log_retrieval_error(query, str(e))
        raise e

# LCEL Chain with logging
rag_chain = (
    {
        "context": RunnableLambda(retrieve_documents) | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    }
    | prompt
    | (lambda x: call_llm(x.to_string()))
    | StrOutputParser()
)

# 🔥 Main function
def ask_question(query: str):
    return rag_chain.invoke(query)
