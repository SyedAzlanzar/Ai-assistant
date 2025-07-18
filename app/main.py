from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer

# Import routers
from app.api.v1.routes import auth, user, ai

app = FastAPI(title="AI Assistant API")

# Mount static files (resumes and fonts if needed)
app.mount("/fonts", StaticFiles(directory="assets/fonts"), name="fonts")

# Define OAuth2 scheme for protected routes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Create and include routers
# Public router for register and login
from fastapi import APIRouter

public_router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])
public_router.post("/register")(auth.register)
public_router.post("/login")(auth.login)
app.include_router(public_router)

# Protected router for onboard and chat
protected_router = APIRouter(
    prefix="/api/v1",
    tags=["Protected"],
    dependencies=[Depends(oauth2_scheme)]
)
protected_router.post("/user/onboard")(user.onboard_user)
protected_router.post("/ai/chat")(ai.chat)
app.include_router(protected_router)

# Customize OpenAPI to show proper security scheme
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title="AI Assistant API",
        version="1.0",
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    schema["security"] = [{"BearerAuth": []}]
    # Remove lock from public routes
    for path in ["/api/v1/auth/register", "/api/v1/auth/login"]:
        if path in schema["paths"]:
            for op in schema["paths"][path].values():
                op.pop("security", None)
    app.openapi_schema = schema
    return app.openapi_schema

app.openapi = custom_openapi
