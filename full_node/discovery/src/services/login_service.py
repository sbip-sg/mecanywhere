import requests
import json
import random
import string
from .database import get_session, users
from sqlalchemy import select, column
import nacl.utils
import nacl.signing
import ecdsa
import base64
import hashlib

def convert_to_bytes(public_key_str):
    # print(type(public_key_str))
    # byte_values = [int(x) for x in str(public_key_str).split(',')]
    # print(byte_values)
    byte_array = bytearray(public_key_str)
    return bytes(byte_array)
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
        
    def verify_response(self, message: str, signature: str, publicKey: str):
        is_authenticated = self.verify_signature(message, signature, publicKey)
        print(is_authenticated)
        return is_authenticated

    # def verify_response(self, did: str, signedChallenge: str, challenge: str):
    #     public_key = self.get_public_key_wallet(did)
    #     is_authenticated = self.verify_signature(message, signature, publicKey)
    #     return is_authenticated
    def verify_signature(self, message, signature, public_key):
        # message = b'Hello, World!'
        print("signature1", list(bytes.fromhex(signature)))

        # hash = hashlib.sha256(message.encode()).hexdigest()
        # messageBytes = bytearray.fromhex(hash)
        # print("private_key", list(bytes.fromhex(private_key)))
        # print("public_key", list(bytes.fromhex(public_key)))

        # print("node signature", list(bytes.fromhex(signature)))
        # print("messageBytes", list(messageBytes))
        # print("message", list(message))
        # print("messagesha", hashlib.sha256(message.encode('utf-8')))
        # print("signature", signature)
        # print("public_key", public_key)
        # print("firstsingature", signature)
        # message = '48656c6c6f2c20576f726c6421'
        

        # sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve=ecdsa.SECP256k1)
        # signature = sk.sign(messageBytes)
        # signature_deterministic = sk.sign_deterministic(message)
        # hex_signature = signature.hex()
        # hex_signature_deterministic = signature_deterministic.hex()
        # print("hex_signature", hex_signature)
        # print("messageBytes", list(messageBytes))
        # print("python signature", list(signature))
        # print("python signature_deterministic", list(signature_deterministic))

        # print('sk', sk)
        # signature = sk.sign(bytes.fromhex(message))
        # message = b'Everything should be made as simple as possible, but not simpler.'
        # private_key_buffer = bytearray.fromhex('0000000000000000000000000000000000000000000000000000000000000001') 

        message = message.encode()
        # private_key = bytes.fromhex('1dffa82ec80257075aa18e2ce0caad46476ad80c9f89369f93dbe87c9cba7b05')
        # digest = hashlib.sha3_256()
        # digest.update(message)
        # hash = digest.digest()
       
        # sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1) 
        # signature = sk.sign_digest_deterministic(hash, hashfunc=hashlib.sha256)
        print("signature2", list(bytes.fromhex(signature)))
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1, hashfunc=hashlib.sha3_256)
        # print("message", list(message))
        try:
            vk.verify(bytes.fromhex(signature), message)
            print("yes")
            return True
        except ecdsa.BadSignatureError:
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

    