import os
from dotenv import load_dotenv

from groq import Groq

from pinecone import Pinecone

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


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
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

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

# 🔹 Format documents
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])


# 🔥 LCEL Chain
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | (lambda x: call_llm(x.to_string()))
    | StrOutputParser()
)

# 🔥 Main function
def ask_question(query: str):
    return rag_chain.invoke(query)
