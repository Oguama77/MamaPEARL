from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, prediction, image, variables

# Create FastAPI app
app = FastAPI(title="Medical AI Assistant", description="AI-powered medical assistant for preeclampsia risk assessment")

# Add CORS middleware to allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

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