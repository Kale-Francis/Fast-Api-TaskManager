from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:StrongPassword123!@localhost/fastapi_tasks"

engine = create_engine(DATABASE_URL) # sqlalchemy engine

Base = declarative_base() # Base for our declarative models

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(255), nullable=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)