
from sqlmodel import SQLModel, Session, create_engine


# todo: Should read from .env
#  Database URL
SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mypassword@localhost:1212/py"

# Create the engine to connect to PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Read Models




# Create tables
SQLModel.metadata.create_all(bind=engine)

# Dependency to get a session
def get_session():
    with Session(engine) as session:
        yield session
