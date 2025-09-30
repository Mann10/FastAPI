from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


engine=create_engine('sqlite:///./todosapp.db')

SessionLocal=sessionmaker(autoflush=False, autocommit=False , bind=engine)
Base=declarative_base()