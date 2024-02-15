from pydantic import BaseModel, Field

class Task(BaseModel):
    ipfs_sha256: bytes
    input_hash: bytes
    size: int
    tower_address: str
    host_address: str
    owner: str
    start_block: int
    block_timeout_limit: int
    fee: float
