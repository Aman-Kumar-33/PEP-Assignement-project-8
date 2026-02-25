from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# This will create a file named "sql_app.db" in your root folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# connect_args={"check_same_thread": False} is required only for SQLite in FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# This creates a database session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All our database models will inherit from this Base class
Base = declarative_base()

# We will use this dependency later to give our API endpoints access to the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()