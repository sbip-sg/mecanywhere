from pydantic import BaseModel, Field

class SendMessageResponse(BaseModel):
    success: bool = Field(..., title="Success", description="Whether the message was sent successfully.")
    msg: str = Field(None, title="Message", description="The message of the reply of the host.")
