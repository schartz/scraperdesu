from pydantic import BaseModel, Field


class ScrapeMessagePayload(BaseModel):
    company_id: int = Field(default=-1)
    user_id: int = Field(default=-1)
    website_url: str = Field(default="")


class RAGIngestMessagePayload(BaseModel):
    company_id: int = Field(default=-1)
    user_id: int = Field(default=-1)
    website_url: str = Field(default="")


class AMQMessage(BaseModel):
    message_type: int = 1
    payload: dict = {}


#################################################
# Below are schemas for messages to be sent     #
#################################################


class ScrapeUpdateMessagePayload(BaseModel):
    company_id: int = Field(default=-1)
    user_id: int = Field(default=-1)
    website_url: str = Field(default="")
    total_pages: int = Field()
    scraped_pages: int = Field()
    is_done: bool = Field(default=False)


class ScrapeUpdateMessage(BaseModel):
    message_type: int = 101
    payload: ScrapeUpdateMessagePayload = Field()
