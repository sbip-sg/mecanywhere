from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from models.db_schema import AccountModel
from models.requests import CreateAccountRequest
from exceptions.http_exceptions import InternalServerException
from services.database import Database


class AccountService:
    def __init__(self, db_session: Database):
        self.db = db_session

    def create_user(self, request: CreateAccountRequest):
        try:
            self.db.create_user(request)
            user_data = {"username": request.username}
            return user_data
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "IntegrityError: User already exists."
            )
        except Exception as e:
            self.db.rollback()
            raise InternalServerException(f"Error: Failed to create user. {str(e)}")

    def get_user(self, account: AccountModel):
        try:
            user = self.db.get_user(account.username, account.password)
            return user
        except Exception as e:
            self.db.rollback()
            raise InternalServerException(f"Error: Failed to verify user. {str(e)}")

    def delete_user(self, account: AccountModel):
        try:
            self.db.delete_user(account.username, account.password)
            user_data = {"username": account.username}
            return user_data
        except Exception as e:
            self.db.rollback()
            raise InternalServerException(f"Error: Failed to delete user. {str(e)}")

    def is_user(self, account: AccountModel):
        try:
            user = self.db.get_user(account.username, account.password)
            return user is not None
        except Exception as e:
            self.db.rollback()
            raise InternalServerException(f"Error: Failed to verify user. {str(e)}")

    def update_did_and_pubkey(self, account: AccountModel, did: str, pubkey: str):
        try:
            self.db.update_did_and_pubkey(account.username, account.password, did, pubkey)
        except Exception as e:
            self.db.rollback()
            raise InternalServerException(f"Error: Failed to update DID. {str(e)}")

    def get_claims(self, account: AccountModel):
        try:
            claims = self.db.get_claims(account.username, account.password)
            return claims
        except Exception as e:
            self.db.rollback()
            raise InternalServerException(f"Error: Failed to get claims. {str(e)}")
