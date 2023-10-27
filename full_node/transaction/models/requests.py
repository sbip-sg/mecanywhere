from pydantic import BaseModel, Field

from models.task_metadata_input import TaskMetadataInput

class RecordTaskRequest(BaseModel):
    client_did: str = Field(
        ...,
        example="did:meca:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f",
    )
    client_po_did: str = Field(
        ...,
        example="did:meca:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f",
    )
    host_did: str = Field(
        ...,
        example="did:meca:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f",
    )
    host_po_did: str = Field(
        ...,
        example="did:meca:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f",
    )
    task_metadata: TaskMetadataInput


class UpdateTaskRequest(BaseModel):
    client_did: str = Field(
        ...,
        example="did:meca:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f",
    )
    client_po_did: str = Field(
        ...,
        example="did:meca:0x0fa21fd3d11d2cd5e6cdef2c7cd6531a25a5964f",
    )
    task_metadata: TaskMetadataInput