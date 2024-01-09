import requests

did_input = {"publicKey": "9162489900438906348702968436157779450275819589845486784832046751964054847774610311218195072132906483269992698213206439837565459982787113366244600208153925"}
cpt_input = {
"claim": {
    "title": "cpt",
    "description": "this is cpt",
    "properties": {
      "name": {
        "type": "string",
        "description": "the name of certificate owner"
      },
      "gender": {
        "enum": [
          "F",
          "M"
        ],
        "type": "string",
        "description": "the gender of certificate owner"
      },
      "age": {
        "type": "number",
        "description": "the age of certificate owner"
      }
    },
    "required": [
      "name",
      "age"
    ]
  },
  "publisher": "did:meca:0x52c328ef8b382b1d71cc262b868d803a137ab8d8"
}
vc_input = {
  "claimData": {
    "DID": "did:meca:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f",
    "name": "Chai",
    "gender": "M",
    "age": 29
  },
  "cptId": 2000000,
  "issuer": "did:meca:0x52c328ef8b382b1d71cc262b868d803a137ab8d8"
}

did_response = requests.post('http://localhost:8080/api/v1/did/create', headers={'Content-Type': 'application/json'}, json=did_input)
print("DID creation response:", did_response.json())
print()
cpt_response = requests.post('http://localhost:9090/api/v1/cpt/register', headers={'Content-Type': 'application/json'}, json=cpt_input)
print("Schema creation response:", cpt_response.json())
print()
vc_response = requests.post('http://localhost:9090/api/v1/credential/create', headers={'Content-Type': 'application/json'}, json=vc_input)
print("VC creation response:", vc_response.json())
print()
