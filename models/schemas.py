from pydantic import BaseModel, Field


class ScrapeMessagePayload(BaseModel):
    company_id: int = Field(default=-1)
    user_id: int = Field(default=-1)
    website_url: str = Field(default="")


class AMQMessage(BaseModel):
    message_type: int = 1
    payload: dict = {}
