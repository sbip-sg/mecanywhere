
from sqlalchemy.exc import IntegrityError
import requests
import json
from .database import get_session, users

class AccountCreationService:
    def __init__(self):
        self.session = get_session()

    def create_user(self, email: str, password: str, public_key: str, public_key_wallet: str):
        print(email)
        print(password)
        print(public_key)
        print(public_key_wallet)
        try:
            did = self.create_did(public_key)
            print(did)
            if did:
                credential = self.create_credential(did)
                if credential:
                    new_user = users.insert().values(email=email, password=password, did=did, public_key_wallet=public_key_wallet)
                    self.session.execute(new_user)
                    self.session.commit()
                    print("User created successfully.", new_user)
                    user_data = {
                        "email": email,
                        "did": did,
                        "credential": credential,
                    }
                    return user_data
                else:
                    raise Exception("Failed to create credential from public key")
            else:
                raise Exception("Failed to create DID from public key")
        except IntegrityError:
            self.session.rollback()
            raise Exception("Error: User already exists.")
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error: Failed to create user. {str(e)}")

    def create_did(self, public_key: str) -> str:
        try:
            payload = {
                "publicKey": public_key
            }
            response = requests.post("http://localhost:8080/api/v1/did/create", json=payload)
            if response.status_code == 200:
                data = json.loads(response.content.decode('utf-8'))
                print(data)
                did = data['result']['did']
                print(did)
                return did
            else:
                return None
        except requests.exceptions.RequestException as e:
            raise Exception("Error: Failed to make a request to the DID creation endpoint.")
        except ValueError as e:
            raise Exception("Error: Failed to parse the response from the DID creation endpoint.")
        except KeyError as e:
            raise Exception("Error: Invalid response received from the DID creation endpoint.")
        except Exception as e:
            raise Exception(f"Error: Failed to create DID. {str(e)}")

    def create_credential(self, did: str) -> str:
        try:
            payload = {
                "claimData": {
                    "DID": did,
                    "name": "Chai",
                    "gender": "M",
                    "age": 29
                },
                "cptId": 2000000,
                "issuer": "did:meca:0x52c328ef8b382b1d71cc262b868d803a137ab8d8"
            }
            response = requests.post("http://localhost:8080/api/v1/credential/create", json=payload)
            if response.status_code == 200:
                data = json.loads(response.content.decode('utf-8'))
                return data
            else:
                return None
        except requests.exceptions.RequestException as e:
            raise Exception("Error: Failed to make a request to the credential creation endpoint.")
        except ValueError as e:
            raise Exception("Error: Failed to parse the response from the credential creation endpoint.")
        except KeyError as e:
            raise Exception("Error: Invalid response received from the credential creation endpoint.")
        except Exception as e:
            raise Exception(f"Error: Failed to create credential. {str(e)}")