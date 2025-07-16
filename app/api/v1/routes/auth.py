from fastapi import APIRouter, HTTPException, Depends
from fastapi import status
from pydantic import BaseModel, EmailStr, Field
from app.db.mongodb import db
from app.db.models import User
from app.core.security import hash_password, verify_password, create_access_token, decode_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", scheme_name="BearerAuth")
class RegisterSchema(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    accessToken: str
    userData: User


@router.post("/register")
async def register(data: RegisterSchema):
    try:
        # Check if email already exists
        if await db.users.find_one({"email": data.email}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

        # Hash password and insert new user
        hashed = hash_password(data.password)
        await db.users.insert_one({
            "email": data.email,
            "name": data.name,
            "password": hashed,
            "role": data.role
        })

        return {"message": "User registered successfully"}

    except HTTPException:
        # Re-raise known HTTP errors to be handled by FastAPI
        raise
    except Exception as e:
        # Log or print error for debugging
        print(f"Internal error during registration: {e}")
        # Return a generic internal server error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during user registration."
        )


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginSchema):
    try:
        user_doc = await db.users.find_one({"email": data.email})
        if not user_doc or not verify_password(data.password, user_doc["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        token = create_access_token(
            subject=user_doc["email"], role=user_doc["role"])

        # Sanitize user data
        user_resp = User(**user_doc)

        return {"accessToken": token, "userData": user_resp}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # 1. Decode and verify the provided JWT token
        payload = decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
        # 2. Fetch user from database using subject (email)
        u = await db.users.find_one({"email": payload["sub"]})
        if not u:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return User(**u)

    except HTTPException:
        # Pass through known HTTP exceptions
        raise
    except Exception as e:
        # Log unexpected exceptions for debugging
        print(f"Internal error validating current user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during token validation."
        )
