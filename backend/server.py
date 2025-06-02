from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import json
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dataset_generator import HotelReviewDatasetGenerator

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Hotel Review Dataset Generator")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Global variables for tracking generation progress
generation_status = {
    "is_running": False,
    "progress": 0,
    "total": 0,
    "current_phase": "",
    "completed": False,
    "files_created": []
}

# Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class DatasetGenerationRequest(BaseModel):
    total_reviews: int = 750000
    chunk_size: int = 50000
    output_dir: str = "dataset_parts"

class GenerationStatus(BaseModel):
    is_running: bool
    progress: int
    total: int
    current_phase: str
    completed: bool
    files_created: List[str]

# Dataset generator instance
generator = HotelReviewDatasetGenerator()

@api_router.get("/")
async def root():
    return {"message": "Hotel Review Dataset Generator API"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

@api_router.get("/generation/status", response_model=GenerationStatus)
async def get_generation_status():
    """Get current dataset generation status"""
    return GenerationStatus(**generation_status)

@api_router.post("/generation/start")
async def start_generation(request: DatasetGenerationRequest, background_tasks: BackgroundTasks):
    """Start dataset generation in background"""
    if generation_status["is_running"]:
        raise HTTPException(status_code=409, detail="Generation already in progress")
    
    # Reset status
    generation_status.update({
        "is_running": True,
        "progress": 0,
        "total": request.total_reviews,
        "current_phase": "Initializing",
        "completed": False,
        "files_created": []
    })
    
    # Start background task
    background_tasks.add_task(generate_dataset_background, request)
    
    return {"message": "Dataset generation started", "total_reviews": request.total_reviews}

async def generate_dataset_background(request: DatasetGenerationRequest):
    """Background task for dataset generation"""
    try:
        # Update status
        generation_status["current_phase"] = "Generating reviews"
        
        # Generate the dataset
        reviews = generator.generate_balanced_dataset(request.total_reviews)
        
        generation_status["progress"] = len(reviews)
        generation_status["current_phase"] = "Splitting and saving files"
        
        # Split and save
        file_paths = generator.split_and_save_dataset(
            reviews, 
            request.chunk_size, 
            request.output_dir
        )
        
        generation_status["current_phase"] = "Generating documentation"
        
        # Generate README
        readme_path = generator.generate_readme(
            len(reviews), 
            len(file_paths), 
            request.output_dir
        )
        
        file_paths.append(readme_path)
        
        # Update final status
        generation_status.update({
            "is_running": False,
            "current_phase": "Completed",
            "completed": True,
            "files_created": file_paths
        })
        
        print(f"Dataset generation completed! Generated {len(reviews)} reviews in {len(file_paths)-1} files")
        
    except Exception as e:
        generation_status.update({
            "is_running": False,
            "current_phase": f"Error: {str(e)}",
            "completed": False
        })
        print(f"Error in dataset generation: {str(e)}")

@api_router.get("/generation/sample")
async def get_sample_review():
    """Get a sample generated review"""
    try:
        sample = generator.generate_single_review(1)
        return sample
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating sample: {str(e)}")

@api_router.get("/generation/aspects")
async def get_covered_aspects():
    """Get list of all aspects covered in the dataset"""
    return {
        "total_aspects": len(generator.aspect_mappings),
        "aspects": generator.aspect_mappings
    }

@api_router.post("/generation/test-batch")
async def generate_test_batch(size: int = 100):
    """Generate a small test batch to verify quality"""
    if size > 1000:
        raise HTTPException(status_code=400, detail="Test batch size cannot exceed 1000")
    
    try:
        reviews = []
        for i in range(1, size + 1):
            review = generator.generate_single_review(i)
            reviews.append(review)
        
        # Save test batch
        os.makedirs("test_batch", exist_ok=True)
        test_file = "test_batch/test_reviews.json"
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, indent=2, ensure_ascii=False)
        
        return {
            "message": f"Generated {len(reviews)} test reviews",
            "file": test_file,
            "sample": reviews[:3]  # Return first 3 as sample
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating test batch: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
