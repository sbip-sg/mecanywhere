from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from models.account import AccountModel
from services.database import Database


class AccountService:
    def __init__(self, db_session: Database):
        self.db = db_session

    def create_user(self, account: AccountModel):
        try:
            self.db.create_user(account.did, account.username, account.password)
            user_data = {"username": account.username, "did": account.did}
            return user_data
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "IntegrityError: User already exists."
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Error: Failed to create user. {str(e)}",
            )

    def verify_user(self, account: AccountModel):
        try:
            verified = self.db.verify_user(
                account.did, account.username, account.password
            )
            return verified
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Error: Failed to verify user. {str(e)}",
            )

    def delete_user(self, account: AccountModel):
        try:
            self.db.delete_user(account.did, account.username, account.password)
            user_data = {"username": account.username, "did": account.did}
            return user_data
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                f"Error: Failed to delete user. {str(e)}",
            )
