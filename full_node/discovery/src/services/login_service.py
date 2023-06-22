import random
import string
import ecdsa
import hashlib

def convert_to_bytes(public_key_str):
    byte_array = bytearray(public_key_str)
    return bytes(byte_array)

class LoginService:
    def __init__(self):
        pass
    
    def create_challenge(self):
        # did_doc = self.resolve_did(did)
        challenge = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        return challenge
        
    def verify_response(self, message: str, signature: str, publicKey: str):
        is_authenticated = self.verify_signature(message, signature, publicKey)
        return is_authenticated

    def verify_signature(self, message, signature, public_key):
        # string to byte
        message = message.encode()
        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key), curve=ecdsa.SECP256k1, hashfunc=hashlib.sha3_256)
        try:
            vk.verify(bytes.fromhex(signature), message)
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

    