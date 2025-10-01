from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from .models import ValidationRequest, ValidationResponse, HealthResponse
from .validator import MarketplaceValidator

# Load environment variables
# load_dotenv()  # Load .env
load_dotenv('.env.local')  # Also try .env.local

# Initialise FastAPI app
app = FastAPI(
    title="Marketplace Validator API",
    description="Credit card listing validation API for marketplace compliance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialise validator
try:
    validator = MarketplaceValidator()
except ValueError as e:
    print(f"Warning: {e}")
    validator = None

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if validator else "degraded",
        version="1.0.0"
    )

@app.post("/validate", response_model=ValidationResponse)
async def validate_listing(request: ValidationRequest):
    """
    Validate a credit card listing against marketplace standards
    
    - **listing**: The credit card listing text to validate
    
    Returns validation results including compliance status, issues, and suggestions.
    """
    if not validator:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Validator service is not available. Please check API configuration."
        )
    
    try:
        # Validate the listing
        result = validator.validate_listing(request.listing)
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Validation failed: {str(e)}"
        )

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Marketplace Validator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
