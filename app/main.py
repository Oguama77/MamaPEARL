from fastapi import FastAPI
from app.routes import chat, prediction, image, variables

# Create FastAPI app
app = FastAPI(title="Medical AI Assistant", description="AI-powered medical assistant for preeclampsia risk assessment")

@app.get("/")
async def welcome():
    """Welcome endpoint"""
    return {
        "message": "Welcome to the Medical AI Assistant API",
        "description": "AI-powered medical assistant for preeclampsia risk assessment",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat",
            "prediction": "/prediction", 
            "image": "/image",
            "variables": "/variables",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

# Include routers
app.include_router(chat.router)
app.include_router(prediction.router)
app.include_router(image.router)
app.include_router(variables.router) 