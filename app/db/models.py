from typing import Any, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler):
        return core_schema.no_info_plain_validator_function(cls.validate)

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(str(v))

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {'type': 'string'}


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    name: str
    password: str
    role: str

    model_config = {"populate_by_name": True}

    # ✅ Serialize id (ObjectId -> str)
    @field_serializer("id")
    def serialize_id(self, id_val: ObjectId) -> str:
        return str(id_val)

    # 📦 Exclude password from output
    @field_serializer("password")
    def _exclude_password(self, password: Any) -> None:
        # Returning None ensures it's not serialized
        return None
    

class UserOnboarding(BaseModel):
    tech_stack: str = Field(..., description="Comma-separated list of user skills")
    title: str = Field(..., description="Professional title")
    resume_url: Optional[str] = Field(None, description="URL to the uploaded resume file")
    user_id: PyObjectId = Field(..., alias="_id", description="ID of the user being onboarded")

    model_config = {"populate_by_name": True}

    # ✅ Serialize user_id (ObjectId -> str)
    @field_serializer("user_id")
    def serialize_user_id(self, user_id_val: ObjectId) -> str:
        return str(user_id_val)
    