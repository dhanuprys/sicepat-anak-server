from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from app.api import auth, profile, children, diagnose
from app.database import engine
from app.models import Base
from app.predictor import initialize_predictor

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize stunting predictor
print("🚀 Starting Stunting Checking App...")
predictor = initialize_predictor()

# Create FastAPI app
app = FastAPI(
    title="Stunting Checking App",
    description="API untuk aplikasi deteksi stunting pada anak",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(children.router, prefix="/api")
app.include_router(diagnose.router, prefix="/api")

# Mount static files for reports
app.mount("/reports", StaticFiles(directory="reports"), name="reports")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Stunting Checking App API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
