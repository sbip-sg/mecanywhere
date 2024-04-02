from pydantic import BaseModel, Field

class SendMessageRequest(BaseModel):
    taskId: str = Field(..., title="Task ID", description="The ID of the task on chain.")
    message: str = Field(None, title="Message", description="The message to send to the host.")
