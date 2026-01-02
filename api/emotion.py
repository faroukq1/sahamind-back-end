from fastapi import APIRouter, HTTPException
from schemas.emotion import EmotionAnalyzeRequest, EmotionAnalyzeResponse
from services.llm_service import analyze_emotions

router = APIRouter(prefix="/emotion", tags=["emotion"])


@router.post("/analyze", response_model=EmotionAnalyzeResponse)
def analyze_emotion(data: EmotionAnalyzeRequest):
    if not data.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    emotions = analyze_emotions(data.text)
    return {"emotions": emotions}
