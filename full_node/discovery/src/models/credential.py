from pydantic import BaseModel, Extra, Field


class CredentialModel(BaseModel):
    credential: dict = Field(
        ...,
        example={
            "credential": {
                "context": "https://www.w3.org/2018/credentials/v1",
                "id": "234508ed-fc5b-4ea4-88ac-f04bc657f470",
                "cptId": 2000000,
                "issuer": "did:bdsv:0x52c328ef8b382b1d71cc262b868d803a137ab8d8",
                "issuanceDate": 1680058078,
                "expirationDate": 4833658078,
                "claim": {
                    "gender": "M",
                    "name": "Chai",
                    "DID": "did:bdsv:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f",
                    "age": 29,
                },
                "proof": {
                    "creator": "did:bdsv:0x52c328ef8b382b1d71cc262b868d803a137ab8d8",
                    "salt": {
                        "gender": "ZZijO",
                        "name": "6fLwp",
                        "DID": "cXQ86",
                        "age": "FjOSj",
                    },
                    "created": 1680058078,
                    "type": "Secp256k1",
                    "signatureValue": "zNDJ6NiFvu0yoFYBx7V3ZZVPaBPEMvqBieHbdhUFb8t3YWzRvje5dm8LM8p+OJ85Gq26u+yITTCkGwQlzUVKZxs=",
                },
                "type": ["VerifiableCredential", "original"],
                "signature": "zNDJ6NiFvu0yoFYBx7V3ZZVPaBPEMvqBieHbdhUFb8t3YWzRvje5dm8LM8p+OJ85Gq26u+yITTCkGwQlzUVKZxs=",
                "hash": "0x066d5c0edf9808c11ce4a45f5679b9cba9dacbbc99800f362063887d8ac83ca6",
                "signatureThumbprint": '{"claim":{"DID":"did:bdsv:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f","age":29,"gender":"M","name":"Chai"},"context":"https://www.w3.org/2018/credentials/v1","cptId":2000000,"expirationDate":4833658078,"id":"234508ed-fc5b-4ea4-88ac-f04bc657f470","issuanceDate":1680058078,"issuer":"did:bdsv:0x52c328ef8b382b1d71cc262b868d803a137ab8d8","type":["VerifiableCredential","original"]}',
                "salt": {
                    "gender": "ZZijO",
                    "name": "6fLwp",
                    "DID": "cXQ86",
                    "age": "FjOSj",
                },
                "credentialType": "ORIGINAL",
                "proofType": "Secp256k1",
            }
        },
    )

    class Config:
        extra = Extra.allow
