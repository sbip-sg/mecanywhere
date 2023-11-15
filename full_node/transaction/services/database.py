from sqlalchemy import (
    Float,
    UniqueConstraint,
    create_engine,
    Column,
    Integer,
    String,
    MetaData,
    Table,
    or_
)
from sqlalchemy.orm import sessionmaker

from config import Config
from models.task_metadata import Resources, TaskMetadataInput


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
            Column("resource_cpu", Integer, nullable=False),
            Column("resource_memory", Integer, nullable=False),
            Column("transaction_start_datetime", Integer, nullable=False),
            Column("transaction_end_datetime", Integer, nullable=False),
            Column("task_name", String(255), nullable=False),
            Column("duration", Integer, nullable=False),
            Column("price", Float, nullable=False),
            Column("po_did", String(255), nullable=False),
            Column("host_did", String(255), nullable=False),
            Column("host_po_did", String(255), nullable=False),
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

    def filter_by_host_did(self, did: str):
        return self.session.query(self.transactions).filter_by(host_did=did).all()

    def filter_by_po_did(self, did: str):
        return self.session.query(self.transactions).filter(or_(self.transactions.c.po_did==did, self.transactions.c.host_po_did==did)).all()
    
    def get_transaction(self, transaction_id: str, did: str):
        return self.session.query(self.transactions).filter_by(transaction_id=transaction_id, did=did).first()

    def add_without_commit(
        self,
        task_metadata: TaskMetadataInput,
        did: str,
        price: float,
        po_did: str,
        host_did: str,
        host_po_did: str,
    ):
        metadata_dict = self.flatten_input(task_metadata)
        new_transaction = self.transactions.insert().values(
            **metadata_dict,
            did=did,
            price=price,
            po_did=po_did,
            host_did=host_did,
            host_po_did=host_po_did,
        )
        self.session.execute(new_transaction)

    def update_without_commit(
        self,
        task_metadata: TaskMetadataInput,
        did: str,
        price: float,
        po_did: str,
    ):
        metadata_dict = self.flatten_input(task_metadata)
        self.session.query(self.transactions).filter_by(
            transaction_id=task_metadata.transaction_id, did=did
        ).update(
            {
                **metadata_dict,
                "price": price,
                "po_did": po_did,
            }
        )

    def flatten_input(self, task_metadata: TaskMetadataInput):
        task_metadata_dict = task_metadata.dict()
        task_metadata_dict["resource_cpu"] = task_metadata.resource_consumed.cpu
        task_metadata_dict["resource_memory"] = task_metadata.resource_consumed.memory
        del task_metadata_dict["resource_consumed"]
        return task_metadata_dict
