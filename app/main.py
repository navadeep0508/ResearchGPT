from fastapi import FastAPI
from app.core.config import APP_NAME
from app.api.routes.chat import router as chat_router
from app.api.routes.upload import router as upload_router
from app.auth.auth_routes import router as auth_router


app=FastAPI(title=APP_NAME)
app.include_router(upload_router,prefix="/api/v1", tags=["upload"])
app.include_router(chat_router,prefix="/api/v1",tags=["chat"])

app.include_router(
    auth_router,
    prefix="/api/v1/auth",
    tags=["Auth"]
)
@app.get("/")
async def home():
   return {"message": "ResearchGPT API Running"}
