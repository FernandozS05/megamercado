from sqlmodel import create_engine, Session, SQLModel

db_url = "postgresql://postgres:12345@localhost:5432/megamercado" 
engine = create_engine(db_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
