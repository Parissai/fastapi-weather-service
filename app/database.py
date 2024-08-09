from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./weather.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Provides a database session for dependency injection in FastAPI.

    This generator function yields a database session (`SessionLocal`) 
    for use in API endpoint functions. The session is automatically 
    closed after the request is completed, ensuring proper resource management.

    Yields:
        Session: A SQLAlchemy session object for interacting with the database.

    Example:
        This function is typically used as a dependency in FastAPI routes:

        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
