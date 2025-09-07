"""
Stunting Predictor initialization module
This module initializes the stunting predictor when the application starts
"""

import os
from app.mod.stunting_predictor import create_predictor_from_dataset

# Global predictor instance
predictor = None

def initialize_predictor():
    """Initialize the stunting predictor on application start"""
    global predictor
    
    try:
        print("🚀 Initializing Stunting Predictor...")
        
        # Get the base directory for the app
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Set cache directory
        cache_dir = os.path.join(base_dir, "model_cache")
        
        # Try to create predictor with cache enabled
        predictor = create_predictor_from_dataset(
            use_cache=True, 
            cache_dir=cache_dir
        )
        
        print("✅ Stunting Predictor initialized successfully!")
        
        # Print cache status
        cache_status = predictor.cache_status()
        print(f"📊 Cache status: {cache_status['cache_complete']}")
        print(f"📁 Cache directory: {cache_status['cache_directory']}")
        
        return predictor
        
    except Exception as e:
        print(f"❌ Error initializing predictor: {str(e)}")
        print("⚠️  Using fallback placeholder logic")
        return None

def get_predictor():
    """Get the global predictor instance"""
    global predictor
    return predictor

def is_predictor_ready():
    """Check if predictor is ready to use"""
    global predictor
    return predictor is not None and predictor.is_trained
