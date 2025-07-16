from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form, Depends
import os
import uuid
import aiofiles
from app.db.mongodb import db
from app.api.v1.routes.auth import get_current_user
from app.db.models import User
from pydantic import BaseModel
router = APIRouter()

class OnboardingUserSchema(BaseModel):
    tech_stack: str = Form(..., description="Comma-separated list of user skills")
    title: str = Form(..., description="Professional title")
    resume: UploadFile = File(..., description="Resume file in PDF or DOCX format")
    # current_user: User = Depends(get_current_user)
    

@router.post("/onboard")
async def onboard_user(
    tech_stack: str = Form(..., description="Comma-separated list of user skills"),
    title: str = Form(..., description="Professional title"),
    resume: UploadFile = File(..., description="Resume file in PDF or DOCX format"),
    current_user: User = Depends(get_current_user)
):
    
    try:
        os.makedirs("assets/resumes", exist_ok=True)
        unique_filename = f"{current_user.email}_{uuid.uuid4().hex}_{resume.filename}"
        file_path = os.path.join("assets/resumes", unique_filename)

        # Save resume file
        async with aiofiles.open(file_path, "wb") as f:
            content = await resume.read()
            await f.write(content)

        resume_url = f"/resumes/{unique_filename}"

        # Store additional profile data in DB
        await db.users.update_one(
            {"user_id": current_user.id},
            {"$set": {
                "tech_stack": tech_stack,
                "title": title,
                "resume_url": resume_url
            }}
        )

        return {
            "message": "Onboarding successful.",
            "resume_url": resume_url
        }

    except Exception as e:
        print(f"Onboarding error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during onboarding."
        )