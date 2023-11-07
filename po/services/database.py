from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, select
from sqlalchemy.orm import sessionmaker

from config import Config
from models.claim import ClaimData
from models.requests import CreateAccountRequest


class Database:
    def __init__(self, config: Config):
        engine = create_engine(config.get_db_url())
        self.metadata = MetaData()
        self.users = Table(
            "users",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("did", String(255), unique=True, nullable=True),
            Column("pubkey", String(255), unique=True, nullable=True),
            Column("username", String(255), unique=True, nullable=False),
            Column("password", String(255), nullable=False),
            Column("name", String(255), nullable=False),
            Column("gender", String(1), nullable=False),
            Column("age", Integer, nullable=False),
            extend_existing=True,
        )
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.metadata.create_all(engine)

    def create_database(self):
        self.metadata.create_all()

    def drop_database(self):
        self.metadata.drop_all()

    def rollback(self):
        self.session.rollback()

    def create_user(self, request: CreateAccountRequest):
        new_user = self.users.insert().values(**request.dict())
        self.session.execute(new_user)
        self.session.commit()
        print("User created successfully.", request.username)

    def get_user(self, username: str, password: str):
        user = (
            self.session.query(self.users)
            .filter_by(username=username, password=password)
            .first()
        )
        if user:
            return user
        return None

    def delete_user(self, username: str, password: str):
        self.session.execute(
            self.users.delete().where(
                self.users.c.username == username,
                self.users.c.password == password,
            )
        )
        self.session.commit()
        print("User deleted successfully.")

    def update_did_and_pubkey(self, username: str, password: str, did: str, pubkey: str):
        self.session.execute(
            self.users.update()
            .where(
                self.users.c.username == username,
                self.users.c.password == password,
            )
            .values(did=did, pubkey=pubkey)
        )
        self.session.commit()
        print("User updated DID and pubkey successfully.")

    def get_claims(self, username: str, password: str) -> ClaimData:
        claims = (
            self.session.query(
                self.users.c.did,
                self.users.c.name,
                self.users.c.gender,
                self.users.c.age,
            )
            .filter_by(username=username, password=password)
            .first()
        )
        if claims:
            return ClaimData(*claims)
        return None
