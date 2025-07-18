from fastapi import APIRouter, HTTPException, status, Form, Depends
from fastapi.responses import JSONResponse
from app.db.mongodb import db
from app.api.v1.routes.auth import get_current_user
from app.db.models import User
from pydantic import BaseModel
from bson import ObjectId
router = APIRouter()


class OnboardingUserSchema(BaseModel):
    techStack: str = Form(...,
                          description="Comma-separated list of user skills")
    jobTitle: str = Form(..., description="Professional title")
    currentUser: User = Depends(get_current_user)


@router.post("/onboard")
async def onboard_user(
    techStack: str = Form(...,
                          description="Comma-separated list of user skills"),
    jobTitle: str = Form(..., description="Professional title"),
    currentUser: User = Depends(get_current_user)
):

    try:
        # find user by ID
        user = await db.users.find_one({"_id": currentUser.id})
        if not user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "User not found"}
            )
        # Check if user is already onboarded
        if user.get("is_onboarded", True):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"message": "User is already onboarded."}
            )

        # Store additional profile data in DB
        await db.onboarding_details.insert_one({
            "user_id": ObjectId(currentUser.id),
            "tech_stack": techStack,
            "job_title": jobTitle
        })

        # Update user onboarding status
        await db.users.update_one(
            {"_id": currentUser.id},
            {"$set": {"is_onboarded": True, "is_active": True}}
        )

        user_data = await db.users.find_one({"_id": currentUser.id})
        user = User(**user_data)

        return {
            "message": "Onboarding successful.",
            "user": user.model_dump_public()
        }

    except Exception as e:
        print(f"Onboarding error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during onboarding."
        )
