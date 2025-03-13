from pydantic import BaseModel

class TextRequest(BaseModel):
    text: str 

class TextResponse(BaseModel):
    anonymized_text: str
