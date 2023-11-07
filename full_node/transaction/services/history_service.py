import uuid
from fastapi import HTTPException, status
from exceptions.http_exceptions import InternalServerException
from models.transaction import Transaction
from models.requests import RecordTaskRequest
from services.database import Database
import random
import datetime


class HistoryService:
    def __init__(self, db: Database):
        self.db = db

    def get_did_history(self, did: str, host: bool = False):
        try:
            if host:
                print("Getting host history", did)
                return self.db.filter_by_host_did(did)
            print("Getting history", did)
            return self.db.filter_by_did(did)
        except Exception as e:
            print(f"Error: Failed to add history. {str(e)}")
            self.db.rollback()
            raise InternalServerException(
                f"Error: Failed to add history. {str(e)}"
            )

    def get_transaction(self, did: str, transaction_id: str) -> Transaction:
        try:
            print("Getting transaction", transaction_id, did)
            entry = self.db.get_transaction(transaction_id, did)
            if entry is None:
                return None
            return Transaction(*entry)
        except Exception as e:
            print(f"Error: Failed to get history. {str(e)}")
            self.db.rollback()
            raise InternalServerException(
                f"Error: Failed to get history. {str(e)}"
            )

    def add_did_history(
        self, request: RecordTaskRequest, price: float
    ):
        task_metadata = request.task_metadata
        try:
            self.db.add_without_commit(
                task_metadata.transaction_id,
                request.client_did,
                task_metadata.resource_consumed,
                task_metadata.transaction_start_datetime,
                task_metadata.transaction_end_datetime,
                task_metadata.task_name,
                task_metadata.duration,
                price,
                request.client_po_did,
                request.host_did,
                request.host_po_did,
                task_metadata.network_reliability,
            )
            self.db.commit()
            print("Added history", task_metadata.transaction_id, request.client_did)
        except Exception as e:
            print(f"Error: Failed to add history. {str(e)}")
            self.db.rollback()
            raise InternalServerException(
                f"Error: Failed to add history. {str(e)}"
            )
        
    def update_did_history(
        self, request: RecordTaskRequest, price: float
    ):
        task_metadata = request.task_metadata
        try:
            self.db.update_without_commit(
                task_metadata.transaction_id,
                request.client_did,
                task_metadata.resource_consumed,
                task_metadata.transaction_start_datetime,
                task_metadata.transaction_end_datetime,
                task_metadata.task_name,
                task_metadata.duration,
                price,
                request.client_po_did,
                task_metadata.network_reliability,
            )
            self.db.commit()
            print("Updated history", task_metadata.transaction_id, request.client_did)
        except Exception as e:
            print(f"Error: Failed to add history. {str(e)}")
            self.db.rollback()
            raise InternalServerException(
                f"Error: Failed to add history. {str(e)}"
            )

    def get_po_did_history(self, did: str):
        try:
            return self.db.filter_by_po_did(did)
        except Exception as e:
            print(f"Error: Failed to get history. {str(e)}")
            self.db.rollback()
            raise InternalServerException(
                f"Error: Failed to get history. {str(e)}"
            )

    def add_dummy_history(self, did: str, po_did: str, host: bool = False):
        try:
            if host:
                for i in range(50):
                    start_time = datetime.datetime.now() + datetime.timedelta(
                        days=random.randint(-100, 0)
                    )
                    end_time = start_time + datetime.timedelta(hours=random.randint(1, 20))
                    self.db.add_without_commit(
                        str(uuid.uuid4()),
                        did=str(uuid.uuid4()),
                        resource_consumed=random.randint(1, 100),
                        transaction_start_datetime=int(start_time.timestamp()),
                        transaction_end_datetime=int(end_time.timestamp()),
                        task_name=f"Task {i}",
                        duration=random.randint(1, 60),
                        price=random.uniform(10.0, 100.0),
                        po_did=str(uuid.uuid4()),
                        host_did=did,
                        host_po_did=po_did,
                        network_reliability=random.randint(1, 10),
                    )
            else:
                for i in range(50):
                    start_time = datetime.datetime.now() + datetime.timedelta(
                        days=random.randint(-100, 0)
                    )
                    end_time = start_time + datetime.timedelta(hours=random.randint(1, 20))
                    self.db.add_without_commit(
                        str(uuid.uuid4()),
                        did,
                        resource_consumed=random.randint(1, 100),
                        transaction_start_datetime=int(start_time.timestamp()),
                        transaction_end_datetime=int(end_time.timestamp()),
                        task_name=f"Task {i}",
                        duration=random.randint(1, 60),
                        price=random.uniform(10.0, 100.0),
                        po_did=po_did,
                        host_did=str(uuid.uuid4()),
                        host_po_did=str(uuid.uuid4()),
                        network_reliability=random.randint(1, 10),
                    )
            self.db.commit()
        except Exception as e:
            print(f"Error: Failed to add history. {str(e)}")
            self.db.rollback()
            raise InternalServerException(
                f"Error: Failed to add history. {str(e)}"
            )
