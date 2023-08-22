import csv
import datetime
from sqlalchemy import (
    DateTime,
    Float,
    create_engine,
    Column,
    Integer,
    String,
    MetaData,
    Table,
)
from sqlalchemy.orm import sessionmaker

from config import Config


class Database:
    def __init__(self, config: Config):
        engine = create_engine(config.get_db_url())
        self.metadata = MetaData()
        self.transactions = Table(
            "transactions",
            self.metadata,
            Column("id", String(255), primary_key=True),
            Column("did", String(255), nullable=False),
            Column("resource_consumed", Float, nullable=False),
            Column("session_start_datetime", Integer, nullable=False),
            Column("session_end_datetime", Integer, nullable=False),
            Column("task", String(255), nullable=False),
            Column("duration", Integer, nullable=False),
            Column("price", Float, nullable=False),
            extend_existing=True,
        )
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.metadata.create_all(engine)
        # with open('data.csv', 'r') as f:
        #     csv_reader = csv.reader(f)
        #     next(csv_reader, None)
        #     for row in csv_reader:
        #         self.session.execute(
        #             self.transactions.insert().values(
        #                 id=str(row[0]),
        #                 did=str(row[1]),
        #                 resource_consumed=float(row[2]),
        #                 session_start_datetime=int(row[3]),
        #                 session_end_datetime=int(row[4]),
        #                 task=str(row[5]),
        #                 duration=int(row[6]),
        #                 price=float(0)
        #             )
        #         )
        #     self.session.commit()

    def create_database(self):
        self.metadata.create_all()

    def drop_database(self):
        self.metadata.drop_all()

    def rollback(self):
        self.session.rollback()

    def get_all_from_did(self, did: str):
        return self.session.query(self.transactions).filter_by(did=did).all()
    
    def add(self, session_id: str, did: str, resource_consumed: float, session_start_datetime: int, session_end_datetime: int, task: str, duration: int, price: float):
        new_transaction = self.transactions.insert().values(
                id=session_id,
                did=did,
                resource_consumed=resource_consumed,
                session_start_datetime=session_start_datetime,
                session_end_datetime=session_end_datetime,
                task=task,
                duration=duration,
                price=price
            )
        self.session.execute(new_transaction)
        self.session.commit()
