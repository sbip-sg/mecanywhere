Deployment
===========

We have launched our smart contracts on the Ethereum Sepolia Testnet (address: ``0xE4a7d3086C42e972000066630f38b720AE5A67c0``). You can get free testnet ETH from the `Sepolia Testnet Faucet <https://faucet.sepolia.io/>`__ and use those accounts to interact with the MECAnywhere network.
To configure for Sepolia:

- MECA_BLOCKCHAIN_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/nf3vIJJEKzQWwbKW1UHXvw1aKAeE6B97
- MECA_DAO_CONTRACT_ADDRESS=0xE4a7d3086C42e972000066630f38b720AE5A67c0

The rpc url is also used for deployment to the Sepolia testnet.

To deploy the MECAnywhere contracts on your own network, you can use the scripts in the pymeca repository -> ``pymeca/src/pymeca/scripts/deploy.py``.
