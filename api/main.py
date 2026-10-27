from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.schema import UserRequest, AIResponse
from api.RagEngine import rag_engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "status ok"}

@app.post("/chat", response_model=AIResponse)
async def chat(request: UserRequest):
    answer = rag_engine.get_answer(request.request)
    return AIResponse(ans=answer)