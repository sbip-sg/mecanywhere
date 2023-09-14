from models.task_metadata_input import TaskMetadataInput

class DidRecord(TaskMetadataInput):
    price: float

    class Config:
        orm_mode = True
