from pydantic import BaseModel

class EmotionAnalyzeRequest(BaseModel):
    text: str

class EmotionAnalyzeResponse(BaseModel):
    emotions: dict[str, float]
