from fastapi import APIRouter
from api.models import TextRequest, TextResponse
from anonymization import  FacerAnonymizer 

router = APIRouter()
anonymizer = FacerAnonymizer(False)

@router.post("/anonymize", response_model=TextResponse)
async def anonymize(request: TextRequest):
    anonymized_text, _ = anonymizer.anonymize(request.text)
    return {"anonymized_text": anonymized_text}

@router.post("/desanonymize", response_model=TextResponse)
async def desanonymize(request: TextRequest):
    desanonymized_text = anonymizer.desanonymize(request.text)
    return {"desanonymized_text": desanonymized_text}
