from pydantic import BaseModel, Field, ConfigDict, field_serializer
from typing import Any
from bson import ObjectId
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler


# -------------------- PyObjectId --------------------
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


# -------------------- User Model --------------------
class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    first_name: str
    last_name: str
    country: str
    city: str
    phone_no: str
    is_onboarded: bool = False
    is_active: bool = False
    password: str
    role: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

    @field_serializer("id")
    def serialize_id(self, id_val: ObjectId) -> str:
        return str(id_val)

    def model_dump_public(self):
        """Serialize user object and exclude password."""
        return self.model_dump(exclude={"password"})


# -------------------- OnboardingDetails Model --------------------
class OnboardingDetails(BaseModel):
    user_id: PyObjectId = Field(..., alias="_id", description="ID of the user being onboarded")
    tech_stack: str = Field(..., description="Comma-separated list of user skills")
    job_title: str = Field(..., description="Professional title")

    model_config = ConfigDict(populate_by_name=True)

    @field_serializer("user_id")
    def serialize_user_id(self, user_id_val: ObjectId) -> str:
        return str(user_id_val)
