# api/auth.py
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from api.database import get_db
import api.models as models

load_dotenv()

# 1. Setup Password Hashing. ### pwd_context handles password hashing. (bcrypt is the hashing algorithm --> very secure)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Setup JWT Config
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback_secret_key_change_this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

#  OAuth2 Scheme (Tells Swagger UI to show a "Lock" icon and an Authorize button). ## This tells FastAPI: look for token at /login route. React will send token in header: Authorization: Bearer <token> 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# convert my_password into unreadable form. We save this hashed password in database
def get_password_hash(password):
    # Turns "password123" into a secure hash like "$something..."
    return pwd_context.hash(password)


 # checks if my password matches the save password. return true or false
def verify_password(plain_password, hashed_password):
    # Checks if the typed password matches the hash
    return pwd_context.verify(plain_password, hashed_password)


# Generates the JWT Token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



# This function is used to protect routes. If token is missing or invalid then -> through 401 error. If valid -> return the user object. get_current_user is the ECURITY GUARD
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # Find the user in the database using the email from the token
    user = db.query(models.Customer).filter(models.Customer.email == email).first()
    if user is None:
        raise credentials_exception
    return user