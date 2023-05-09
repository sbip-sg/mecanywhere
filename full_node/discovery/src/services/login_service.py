import requests
import json
import random
import string
from .database import get_session, users
from sqlalchemy import select, column
import nacl.utils
import nacl.signing

class LoginService:
    def __init__(self):
        self.session = get_session()

    def create_challenge(self, email: str, password: str, did: str):
        # did_doc = self.resolve_did(did)
        challenge = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        return challenge
    
    def get_public_key_wallet(self, did: str):
        query = select(column('public_key_wallet')).where(users.c.did == did)
        result = self.session.execute(query).fetchone()
        if result is not None:
            public_key_wallet = result[0]
            return public_key_wallet
        else:
            return None
        
    def verify_response(self, did: str, signedChallenge: str, challenge: str):
        public_key = self.get_public_key_wallet(did)
        is_authenticated = self.verify_signature(challenge, signedChallenge, public_key)
        return is_authenticated

    def verify_signature(self, challenge, signature64, public_key):
        # decode the signature from Base64 to bytes
        signature = nacl.encoding.Base64Encoder.decode(signature64)
        public_key_bytes = bytes.fromhex(public_key)
        # create a VerifyKey object from the public key bytes
        verify_key = nacl.signing.VerifyKey(public_key_bytes)
        # verify the signature using the message and public key
        try:
            verify_key.verify(challenge.encode('utf-8'), signature)
            print("Signature is valid")
            return True
        except nacl.exceptions.BadSignatureError:
            print("Signature is invalid")
            return False
        
    ## resolve from bdsv DID
    # def resolve_did(self, did: str):
    #     try:
    #         headers = {
    #             "Accept": "*/*"
    #         }
    #         url = f"http://localhost:8080/api/v1/did/document/{did}"
    #         response = requests.get(url, headers=headers)
    #         response_json = json.loads(response.text)
    #         return response_json['result']
    #     except requests.RequestException as e:
    #         print(f"An error occurred during the API request: {str(e)}")
    #     except json.JSONDecodeError as e:
    #         print(f"An error occurred while parsing the JSON response: {str(e)}")

    