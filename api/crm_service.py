# This file contains the only functions allowed to touch the database for CRM purposes. The AI will call these functions.
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.database import get_db
from api.schema import UserRegister, UserResponse, Token
from api.auth import get_password_hash, get_current_user, verify_password, create_access_token

import api.models as models

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register", response_model=UserResponse)
def register_user(user: UserRegister, db:Session=Depends(get_db)):
    db_user=db.query(models.Customer).filter(models.Customer.email==user.email).first()

    if db_user:
        raise HTTPException(
            status_code=400, detail="Email Aready Register",

        )

    # Hashed the pass and create user
    hash_pw = get_password_hash(user.password)
    new_user = models.Customer(
        name=user.name,
        email=user.email,
        hashed_password=hash_pw

    )

    # save the mysql
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post('/login', response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    # Find user by email (form_data.username is the email in this form)
    user = db.query(models.Customer).filter(models.Customer.email==form_data.username).first()

    # varify user exists and password is currect 
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate and return the jwt token
    access_token=create_access_token(data={'sub':user.email})
    return {"access_token":access_token, "token_type":"bearer"}


# this is protected route you can see only if you are logged in
@router.get('/me', response_model=UserResponse)
def read_user_me(current_user: models.Customer=Depends(get_current_user)):
    return current_user



# _______________ phase-3 ____________
@router.get('/my-orders')
def get_my_orders(current_user: models.Customer = Depends(get_current_user), db: Session = Depends(get_db)):
    # Secure: We only query orders where the customer_id matches the logged-in user's ID
    orders = db.query(models.Order).filter(models.Order.customer_id == current_user.id).all()

    if not orders:
        return {'message': 'You have no orders'}

    return orders

# Helper function for the chatbot to fetch orders directly
def fetch_user_orders_for_bot(user_id: int, db: Session):
    orders = db.query(models.Order).filter(models.Order.customer_id == user_id).all()

    if not orders:
        return "No order Founds"

    # Formate the database data into a text string the LLM  can read
    order_text=""

    for order in orders:
        # order_text += f"Order: {order.product_name}, status: {order.status}, Amount: ${order.amount}, Date: {order.created_at}\n"


        order_text += f"""Order ID: {order.id}
        Product: {order.product_name}
        Status: {order.status}
        Tracking Number: {order.tracking_number or 'Not available'}
        Amount: ₹{order.amount}
        Order Date: {order.created_at}"""



        return order_text




