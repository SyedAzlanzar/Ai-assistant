from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.api.v1.routes.auth import get_current_user
from app.core.ai import run_ai

router = APIRouter(prefix="/ai", tags=["ai"])

class PromptSchema(BaseModel):
    prompt: str
    userSkills: str = ""  # Optional field for user's skills
    tone: str = "professional"  # Default tone, can be overridden
    applicant: dict = {
        "fullName": "",
        "address": "",
        "email": "",
        "phone": ""
    }
    lng: str = "en"  # Default language, can be overridden

# @router.post("/chat")
# async def chat(data: PromptSchema, user = Depends(get_current_user)):
#     try:
#         reply = run_ai(data.prompt, user.role)
#         return {"reply": reply}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def chat(data: PromptSchema):  # removed auth dependency
    reply = run_ai(data.prompt,data.userSkills,data.tone,data.applicant,lng="en")  # Assuming 'lng' is a language parameter, defaulting to English
    return {"reply": reply}
