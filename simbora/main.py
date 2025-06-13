import os
from typing import Annotated, Optional
from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from langchain_openai import OpenAIEmbeddings
from pydantic import BaseModel
from simbora.agents.supervisor import supervisor

ENDPOINT_QUERY_AI_MAX_SIZE = int(os.getenv("ENDPOINT_QUERY_AI_MAX_SIZE"))
ENDPOINT_EMBEDDING_TEXT_MAX_SIZE = int(os.getenv("ENDPOINT_EMBEDDING_TEXT_MAX_SIZE"))
ENDPOINT_EMBEDDING_MODEL = os.getenv("ENDPOINT_EMBEDDING_MODEL")

class StructuredQuery(BaseModel):
    course: Optional[str] = None
    content: Annotated[str, Query(max_length=ENDPOINT_QUERY_AI_MAX_SIZE)]


app = FastAPI(
    title="Simbora API",
    version="0.1.0"
)

@app.get("/ai")
async def ai(structured_query: StructuredQuery):
    response = supervisor.invoke({"messages": [{"role": "user", "content": structured_query.content}]})
    return response["messages"][-1].content

# FIXME: CORs policy should be set to allow requests from the matriculaai-backend only
@app.post("/embedding")
async def embedding(text: Annotated[str, Query(max_length=ENDPOINT_EMBEDDING_TEXT_MAX_SIZE)]):
    embedder = OpenAIEmbeddings(model=ENDPOINT_EMBEDDING_MODEL)
    return embedder.embed_query(text)

@app.get("/ping")
async def root():
    return "Pong! :)"

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
