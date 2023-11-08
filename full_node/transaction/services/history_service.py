import uuid
from exceptions.http_exceptions import InternalServerException
from models.task_metadata import TaskMetadataInput
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

    def add_did_history(self, request: RecordTaskRequest, price: float):
        task_metadata = request.task_metadata
        try:
            self.db.add_without_commit(
                task_metadata,
                request.client_did,
                price,
                request.client_po_did,
                request.host_did,
                request.host_po_did,
            )
            self.db.commit()
            print("Added history", task_metadata.transaction_id, request.client_did)
        except Exception as e:
            print(f"Error: Failed to add history. {str(e)}")
            self.db.rollback()
            raise InternalServerException(
                f"Error: Failed to add history. {str(e)}"
            )

    def update_did_history(self, request: RecordTaskRequest, price: float):
        task_metadata = request.task_metadata
        try:
            self.db.update_without_commit(
                task_metadata,
                request.client_did,
                price,
                request.client_po_did,
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
                    self.db.add_without_commit(
                        self._random_task_metadata(f"Task {i}"),
                        did=str(uuid.uuid4()),
                        price=random.uniform(10.0, 100.0),
                        po_did=str(uuid.uuid4()),
                        host_did=did,
                        host_po_did=po_did,
                    )
            else:
                for i in range(50):
                    self.db.add_without_commit(
                        self._random_task_metadata(f"Task {i}"),
                        did,
                        price=random.uniform(10.0, 100.0),
                        po_did=po_did,
                        host_did=str(uuid.uuid4()),
                        host_po_did=str(uuid.uuid4()),
                    )
            self.db.commit()
        except Exception as e:
            print(f"Error: Failed to add history. {str(e)}")
            self.db.rollback()
            raise InternalServerException(
                f"Error: Failed to add history. {str(e)}"
            )

    def _random_task_metadata(self, task_name: str):
        start_time = datetime.datetime.now() + datetime.timedelta(
            days=random.randint(-100, 0)
        )
        end_time = start_time + datetime.timedelta(hours=random.randint(1, 20))
        return TaskMetadataInput(
            transaction_id=str(uuid.uuid4()),
            resource_consumed={
                "cpu": random.randint(1, 10),
                "memory": random.randint(1, 100),
            },
            transaction_start_datetime=int(start_time.timestamp()),
            transaction_end_datetime=int(end_time.timestamp()),
            task_name=task_name,
            duration=random.randint(1, 60),
            network_reliability=random.randint(1, 10),
        )
