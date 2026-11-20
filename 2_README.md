# Why you need each one:
> sqlalchemy: 
The main library that creates the engine, sessions, and base.

> pymysql: 
The driver that actually allows Python to talk to MySQL (since your URL says mysql+pymysql://).

> cryptography: 
MySQL 8+ requires this library for secure authentication. If you don't install it, pymysql will throw an error.

> python-dotenv: 
Required because you are using from dotenv import load_dotenv to read your .env file.

> command to run in terminal
# pip install sqlalchemy pymysql cryptography python-dotenv

> database.py
> models.py
> setup_db.py

# ________________________ phase=2 _______________________
Authentication & Security.

# pip install passlib[bcrypt] python-jose[cryptography] python-multipart

> Create api/auth.py  -> # handles all jwt and password logic
 This file contains the logic for hashing, verifying, and creating tokens.

 > Update app/schema.py
 We need schemas to handle the registration and login requests

 > Create api/crm_routes.py
 This is where the actual endpoints live

 > Update app/Main.py 
 (Connect the routes)

How to Test Phase 2:
Start your server: uvicorn app.Main:app --reload


# ______________________ Phase 3: Intelligent Routing & CRM Integration.  ______________

we will build the "Brain" of the chatbot. When a user types a message, the system needs to decide: "Is this a general FAQ question, or is this a question about MY specific account?


Update --> crm_services
> get_my_orders
> fetch_user_orders_for_bot

Update ->  RagEngine.py
