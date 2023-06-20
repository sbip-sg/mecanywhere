from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
from ecdsa import SigningKey, SECP256k1
import json
import os
import pytest

test_app = TestClient(app)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(__location__, 'test_data.json')) as file:
    data = json.load(file)
    credentials = data['credentials']
    tokens = data['tokens']
    message = data['message']
    public_key = data['public_key']
    signature = data['signature']

def test_create_user():
    private_key = SigningKey.generate(curve=SECP256k1)  
    public_key_bytes = private_key.get_verifying_key().to_string()
    public_key_decimal = int.from_bytes(public_key_bytes, 'big')
    response = test_app.post("/create_account/", json={'publicKey': public_key_decimal})
    did = response.json()['did']
    assert response.status_code == 200
    assert did[0:11] == 'did:bdsv:0x'
    assert len(did) == 51

def test_create_challenge():
    response = test_app.post("/create_challenge/", json={'publicKey': 'test'})
    challenge = response.json()
    assert type(challenge) == str
    assert len(challenge) == 16

def test_verify_response():   
    response = test_app.post("/verify_response/", json={'message': message,
                                                        "publicKey": public_key, 
                                                        "signature": signature})
    data = response.json()
    assert data

def test_register_client():
    response = test_app.post("/registration/register_client/", json=credentials)
    data = response.json()
    pytest.tokens = data
    assert len(data['access_token']) == 2087
    assert len(data['refresh_token']) == 2087
    assert data['access_token_type'] == "bearer"
    assert data['refresh_token_type'] == "bearer"
    # need add expiration tests
    
def test_register_host():
    response = test_app.post("/registration/register_host/", json=credentials)
    data = response.json()
    assert len(data['access_token']) == 2087
    assert len(data['refresh_token']) == 2087
    assert data['access_token_type'] == "bearer"
    assert data['refresh_token_type'] == "bearer"
    # need add expiration tests

def test_deregister_client():
    # might want to extract the logic out for generating token
    access_token = pytest.tokens["access_token"]
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    response = test_app.post(
        "/registration/deregister_client/", 
        headers=headers,
        json={"did": credentials["did"]})
    assert response.status_code == 200
    
def test_deregister_host():
    access_token = pytest.tokens["access_token"]
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    response = test_app.post(
        "/registration/deregister_host/", 
        headers=headers,
        json={"did": credentials["did"]})
    assert response.status_code == 200

def test_assign_host():
    access_token = pytest.tokens["access_token"]
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    response = test_app.post(
        "/assign_host/", 
        headers=headers,
        json={"did": credentials["did"]})
    assert "queue" in response.json()

def test_refresh_access():
    refresh_token = pytest.tokens["refresh_token"]
    response = test_app.post("/registration/refresh_access/?refresh_token={}".format(refresh_token))    
    data = response.json()
    assert len(data['access_token']) == 2087
    assert data['access_token_type'] == "bearer"

def test_heartbeat():
    access_token = pytest.tokens["access_token"]
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    response = test_app.post(
        "/heartbeat/", 
        headers=headers,
        json={"did": credentials["did"]})
    assert response.status_code == 200
