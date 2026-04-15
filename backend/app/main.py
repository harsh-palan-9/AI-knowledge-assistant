from fastapi import FastAPI
import logging
from app.routes import document, query, auth
from app.middleware.logging_middleware import LoggingMiddleware

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="AI Knowledge Assistant", description="A platform for RAG (Retrieval-Augmented Generation) applications")

# Add logging middleware
app.add_middleware(LoggingMiddleware)

app.include_router(document.router)
app.include_router(query.router)
app.include_router(auth.router)