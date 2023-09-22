import uuid
from fastapi import HTTPException, status
from models.task_metadata_input import TaskMetadataInput
from services.database import Database
import random
import datetime


class HistoryService:
    def __init__(self, db: Database):
        self.db = db

    def get_did_history(self, did: str):
        try:
            return self.db.filter_by_did(did)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Error: Failed to get history. {str(e)}",
            )

    def add_did_history(
        self, did: str, po_did: str, task_metadata: TaskMetadataInput, price: float
    ):
        session_id = task_metadata.session_id
        resource_consumed = task_metadata.resource_consumed
        session_start_datetime = task_metadata.session_start_datetime
        session_end_datetime = task_metadata.session_end_datetime
        task = task_metadata.task
        duration = task_metadata.duration
        network_reliability = task_metadata.network_reliability
        try:
            self.db.add_without_commit(
                session_id,
                did,
                resource_consumed,
                session_start_datetime,
                session_end_datetime,
                task,
                duration,
                price,
                po_did,
                network_reliability,
            )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Error: Failed to add history. {str(e)}",
            )

    def get_po_did_history(self, did: str):
        try:
            return self.db.filter_by_po_did(did)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Error: Failed to get history. {str(e)}",
            )

    def add_dummy_history(self, did: str, po_did: str):
        try:
            for i in range(50):
                start_time = datetime.datetime.now() + datetime.timedelta(
                    days=random.randint(-100, 0)
                )
                end_time = start_time + datetime.timedelta(hours=random.randint(1, 20))
                self.db.add_without_commit(
                    str(uuid.uuid4()),
                    did,
                    resource_consumed=random.randint(1, 100),
                    session_start_datetime=int(start_time.timestamp()),
                    session_end_datetime=int(end_time.timestamp()),
                    task=f"Task {i}",
                    duration=random.randint(1, 60),
                    price=random.uniform(10.0, 100.0),
                    po_did=po_did,
                    network_reliability=random.randint(1, 10),
                )
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Error: Failed to add history. {str(e)}",
            )
