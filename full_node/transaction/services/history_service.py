from fastapi import HTTPException, status
from services.database import Database


class HistoryService:
    def __init__(self, db: Database):
        self.db = db

    def get_did_history(self, did: str):
        try:
            return self.db.get_all_from_did(did)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Error: Failed to get history. {str(e)}",
            )
        
    def add_did_history(self, did: str, task_metadata: dict, price: float):
        session_id = task_metadata["session_id"]
        resource_consumed = task_metadata["resource_consumed"]
        session_start_datetime = task_metadata["session_start_datetime"]
        session_end_datetime = task_metadata["session_end_datetime"]
        task = task_metadata["task"]
        duration = task_metadata["duration"]
        try:
            self.db.add(session_id, did, resource_consumed, session_start_datetime, session_end_datetime, task, duration, price)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Error: Failed to add history. {str(e)}",
            )
