 #  FastAPI entry point

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
# import local app modules
from api.schema import UserRequest, AIResponse
from api.RagEngine import rag_engine
import api.models as models #### import sqlalchemy models so table can be created
from api.auth import get_current_user
from api.database import get_db

from api.crm_service import router as crm_router, fetch_user_orders_for_bot  # <-- crm_srvices 


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://shopease-ui.vercel.app",
        "http://localhost:5173"
    ],
     allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register the new auth routes
app.include_router(crm_router)

@app.get("/")
def read_root():
    return {"message": "status ok"}

@app.post("/chat", response_model=AIResponse)
async def chat(request: UserRequest, db: Session = Depends(get_db), current_user: models.Customer = Depends(get_current_user)):
    user_question = request.request

    # Ask the llm to route the questions
    route = rag_engine.route_question(user_question)

    if route == "CRM":  ### have to understand this 
        # 2 Fetch real data from mySql securely

        crm_data = fetch_user_orders_for_bot(current_user.id, db)


                # 3. Give the data to the LLM to answer
        
        final_prompt = f"""
        You are a helpful customer support assistant for ShopEase.

        CUSTOMER DATA:
        {crm_data}

        CUSTOMER QUESTION:
        {user_question}

        STRICT RULES:
        1. Answer using ONLY the customer data provided above.
        2. Never invent order IDs, tracking numbers, dates,
        shipping updates, or delivery estimates.
        3. If a tracking number exists, provide it directly.
        4. If information is unavailable, clearly say so.
        5. If there are no orders, explain that no orders
        are associated with the customer's account.
        6. Answer naturally and concisely.

        Answer:
        """

        answer = rag_engine.llm.invoke(final_prompt).content
        return AIResponse(ans=answer)

        
    else:
        # Standard Rag (PDF) Flow
        answer = rag_engine.get_answer(user_question)
        return AIResponse(ans=answer)

# db
@app.get('/db')
def fetch_data():
    return load_data()

