from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker

from config import Config


class Database:
    def __init__(self, config: Config):
        engine = create_engine(config.get_db_url())
        self.metadata = MetaData()
        self.users = Table(
            "users",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("email", String(255), unique=True, nullable=False),
            Column("password", String(255), nullable=False),
            extend_existing=True,
        )
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.metadata.create_all(engine)

    def create_database(self):
        self.metadata.create_all()

    def drop_database(self):
        self.metadata.drop_all()

    def create_user(self, email: str, password: str):
        new_user = self.users.insert().values(email=email, password=password)
        self.session.execute(new_user)
        self.session.commit()
        print("User created successfully.", new_user)

    def rollback(self):
        self.session.rollback()
