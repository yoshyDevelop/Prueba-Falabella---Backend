import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

TURSO_DATABASE_URL = os.environ.get('TURSO_DATABASE_URL')
TURSO_AUTH_TOKEN = os.environ.get('TURSO_AUTH_TOKEN')

if TURSO_DATABASE_URL and TURSO_AUTH_TOKEN:
    db_url = TURSO_DATABASE_URL.replace("libsql://", "").replace("https://", "")
    DATABASE_URL = f"sqlite+libsql://{db_url}?secure=true"
    connect_args = {
        'auth_token': TURSO_AUTH_TOKEN,
        'check_same_thread': False
    }
else:
    DATABASE_URL = "sqlite:///./local.db"
    connect_args = {'check_same_thread': False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
