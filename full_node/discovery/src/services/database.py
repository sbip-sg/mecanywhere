from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./example.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(255), unique=True, nullable=False),
    Column("password", String(255), nullable=False),
    Column("did", String(255), unique=True, nullable=False),
    Column("public_key_wallet", String(255)),
    extend_existing=True,
)

def get_session():
    Session = sessionmaker(bind=engine)
    return Session()

def create_database():
    metadata.create_all()

def drop_database():
    metadata.drop_all()