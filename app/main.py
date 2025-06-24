from fastapi import FastAPI
from app.routes import chat, prediction, image, variables

# Create FastAPI app
app = FastAPI(title="Medical AI Assistant", description="AI-powered medical assistant for preeclampsia risk assessment")

# Include routers
app.include_router(chat.router)
app.include_router(prediction.router)
app.include_router(image.router)
app.include_router(variables.router) 