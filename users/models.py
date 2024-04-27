from pydantic import BaseModel, Field



class Prompt(BaseModel):
    query: str = Field(title="Query", description="Query for model")


