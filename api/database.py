 # Connects to MySQL
import os
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from pathlib import Path



## find the backend directory to locate the .env and certs folder
Backend_DIR = Path(__file__).resolve().parent.parent
load_dotenv(Backend_DIR/".env")

# print("DB_SSL_CA =", os.getenv("DB_SSL_CA"))

# cloud vs local
ssl_ca_cert_text=os.getenv("DB_SSL_CA_CERT")
ssl_ca_file_path=os.getenv("DB_SSL_CA")

if ssl_ca_cert_text:
    # RENDER (Cloud): Use the certificate text directly from the environment variable
    print("Using SSL certificate from environment variable")
    ssl_args={"ssl_ca":ssl_ca_cert_text}

elif ssl_ca_file_path:
    # use the local file path
    print("using ssl certificate from local file")
    ssl_args={"ssl_ca": str(Backend_DIR / ssl_ca_file_path)}
else:
    raise ValueError("Critical: Neither DB_SSL_CA_CERT nor DB_SSL_CA is set!")




# formate: mysql+pymysql://user:password@host:port/dbname
DB_URL = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    host = os.getenv('DB_HOST'),
    port = os.getenv("DB_PORT", "4000"),
    database=os.getenv('DB_NAME'),
    query={
        # "ssl_ca": str(Backend_DIR / os.getenv("DB_SSL_CA")),
        **ssl_args,
        "ssl_verify_cert":"true",
        "ssl_verify_identity":"true"
           }
    )

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# goal: Creates a base class. In our models.py file, our Customer and Order tables will inherit from this Base. 
# SQLAlchemy uses this to map Python classes to actual MySQL tables.

def get_db():
    db = SessionLocal()

    try:
        yield db
        # Purpose: Hands the database session over to the FastAPI route (e.g., to fetch an order).
        # It pauses here until the route finishes its work.

    finally:
        db.close()
         # PURPOSE: Guarantees that the database connection is ALWAYS closed after the route is finished,
          # even if the route crashed with an error. This prevents memory leaks and "too many connections" errors.

