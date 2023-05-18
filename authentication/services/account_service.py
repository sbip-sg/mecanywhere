from sqlalchemy.exc import IntegrityError

from services.database import Database


class AccountService:
    def __init__(self, db_session: Database):
        self.db = db_session

    def create_user(self, email: str, password: str):
        try:
            self.db.create_user(email, password)
            user_data = {"email": email}
            return user_data
        except IntegrityError:
            self.db.rollback()
            raise Exception("Error: User already exists.")
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error: Failed to create user. {str(e)}")
