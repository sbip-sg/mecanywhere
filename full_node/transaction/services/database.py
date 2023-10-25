from sqlalchemy import (
    Float,
    UniqueConstraint,
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
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("transaction_id", String(255), nullable=False),
            Column("did", String(255), nullable=False),
            Column("resource_consumed", Integer, nullable=False),
            Column("transaction_start_datetime", Integer, nullable=False),
            Column("transaction_end_datetime", Integer, nullable=False),
            Column("task_name", String(255), nullable=False),
            Column("duration", Integer, nullable=False),
            Column("price", Float, nullable=False),
            Column("po_did", String(255), nullable=False),
            Column("network_reliability", Integer, nullable=False),
            UniqueConstraint("transaction_id", "did", name="unique_transaction_id_did"),
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

    def commit(self):
        self.session.commit()

    def filter_by_did(self, did: str):
        return self.session.query(self.transactions).filter_by(did=did).all()

    def filter_by_po_did(self, did: str):
        return self.session.query(self.transactions).filter_by(po_did=did).all()

    def add_without_commit(
        self,
        transaction_id: str,
        did: str,
        resource_consumed: float,
        transaction_start_datetime: int,
        transaction_end_datetime: int,
        task_name: str,
        duration: int,
        price: float,
        po_did: str,
        network_reliability: int,
    ):
        new_transaction = self.transactions.insert().values(
            transaction_id=transaction_id,
            did=did,
            resource_consumed=resource_consumed,
            transaction_start_datetime=transaction_start_datetime,
            transaction_end_datetime=transaction_end_datetime,
            task_name=task_name,
            duration=duration,
            price=price,
            po_did=po_did,
            network_reliability=network_reliability,
        )
        self.session.execute(new_transaction)

    def update_without_commit(
        self,
        transaction_id: str,
        did: str,
        resource_consumed: float,
        transaction_start_datetime: int,
        transaction_end_datetime: int,
        task_name: str,
        duration: int,
        price: float,
        po_did: str,
        network_reliability: int,
    ):
        self.session.query(self.transactions).filter_by(
            transaction_id=transaction_id, did=did
        ).update(
            {
                "resource_consumed": resource_consumed,
                "transaction_start_datetime": transaction_start_datetime,
                "transaction_end_datetime": transaction_end_datetime,
                "task_name": task_name,
                "duration": duration,
                "price": price,
                "po_did": po_did,
                "network_reliability": network_reliability,
            }
        )
