import asyncio
import base64
import hashlib
import pathlib
from ecies import encrypt
import requests
from web3 import Web3
import json

import pymeca.utils
from pymeca.user import MecaUser
from pymeca.dao import get_DAO_ADDRESS
from cli import MecaCLI

config = json.load(open("../config/config.json", "r"))
BLOCKCHAIN_URL = config["blockchain_url"]
DAO_CONTRACT_ADDRESS = get_DAO_ADDRESS()
ACCOUNTS = json.load(open(config["accounts_path"], "r"))
OUTPUT_FOLDER = pathlib.Path(config["build_folder"])


def send_message_to_tower(tower_uri, task_id, message):
    tower_uri = tower_uri.replace("localhost", "172.17.0.1", 1)
    tower_url = f"{tower_uri}/send_message"
    res = requests.post(tower_url, json={"taskId": task_id, "message": message})
    if res.status_code != 200:
        print(f"Failed to send message to tower. Status code: {res.status_code}")
        return
    message = json.loads(res.json())
    if "success" in message and message["success"]:
        try:
            # save to png
            OUTPUT_FOLDER.mkdir(exist_ok=True)
            with open(f"{OUTPUT_FOLDER}/output.png", "wb") as f:
                f.write(base64.b64decode(message['msg']))
            print("Message result saved to output.png")
        except Exception as e:
            print(f"Failed to save {message}\n {e}")
    elif "msg" in message and message["msg"]:
        print(f"Host failed to process the message. {message['msg']}")
    else:
        print("Unexpected message from host.", message)
    return message


class MecaUserCLI(MecaCLI):
    def __init__(self):
        web3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_URL))
        meca_user = MecaUser(
            w3=web3,
            private_key=ACCOUNTS["meca_user"]["private_key"],
            dao_contract_address=DAO_CONTRACT_ADDRESS,
        )
        print("Started user with address:", meca_user.account.address)
        super().__init__(meca_user)

    async def run_func(self, func, args):
        if func.__name__ == "send_task_on_blockchain":
            meca_user = self.actor
            ipfs_sha = args[0]
            ipfs_cid = pymeca.utils.cid_from_sha256(ipfs_sha)
            host_address = args[1]
            tower_address = args[2]
            content = args[3]
            task_input = {
                "id": ipfs_cid,
                "input": content,
            }

            # Hash the input and submit it to the blockchain
            input_str = json.dumps(task_input)
            input_hash = hashlib.sha256(input_str.encode("utf-8")).hexdigest()

            success, task_id = meca_user.send_task_on_blockchain(ipfs_sha, host_address, tower_address, input_hash)
            print(f"Task sent to blockchain: task id: {task_id}\n")

            # Send the encrypted input to the tower
            tower_url = meca_user.get_tower_public_uri(tower_address)
            print(f"Sending encrypted input to the tower at {tower_url}")
            host_public_key = meca_user.get_host_public_key(host_address)
            input_enc = encrypt(host_public_key, input_str.encode("utf-8")).hex()
            send_message_to_tower(tower_url, task_id, input_enc)
        else:
            print(func.__name__, ":")
            print(await super().run_func(func, args))


async def main():
    cli = MecaUserCLI()
    meca_user = cli.actor
    cli.add_method(meca_user.get_tasks)
    cli.add_method(meca_user.get_towers_hosts_for_task)
    await cli.start()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
