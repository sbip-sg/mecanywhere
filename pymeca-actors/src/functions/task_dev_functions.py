import ipfs_api
import os

async def add_folder_to_ipfs_host(folder_path: str, ipfs_api_host: str, ipfs_api_port: str):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print("Folder not found.")
        return
    with ipfs_api.ipfshttpclient.connect(
            f"/dns/{ipfs_api_host}/tcp/{ipfs_api_port}/http"
            ) as client:
        for res in client.add(folder_path, recursive=True, cid_version=1, pin=False):
            print(res.as_json())
