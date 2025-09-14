from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import get_current_user
from app.crud import (
    create_diagnose_history, get_diagnose_history_by_id,
    get_diagnose_histories_by_children, get_children_by_id
)
from app.predictor import get_predictor, is_predictor_ready
from app.models import User
from app.schemas import DiagnoseHistoryCreate, DiagnoseHistoryResponse, DiagnoseResult
from app.services.pdf_service import pdf_service

router = APIRouter(prefix="/children", tags=["diagnose"])





@router.post("/{children_id}/diagnose", response_model=DiagnoseHistoryResponse, status_code=status.HTTP_201_CREATED)
def create_diagnose(
    children_id: int,
    diagnose_data: DiagnoseHistoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new diagnose for children"""
    # Verify children belongs to current user
    children = get_children_by_id(db, children_id, current_user.id)
    if not children:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Children not found"
        )
    
    # Get age, height, and gender from input
    age = diagnose_data.age_on_month
    height = diagnose_data.height
    gender = diagnose_data.gender
    
    # Use stunting predictor for diagnosis
    if is_predictor_ready():
        try:
            # Convert gender format from L/P to Laki-laki/Perempuan
            gender_full = "Laki-laki" if gender == "L" else "Perempuan"
            
            print(f"🔍 ML Input: Age={age}m, Gender={gender_full}, Height={height}cm")
            
            # Get prediction from ML model
            prediction_result = get_predictor().predict(age, gender_full, height)
            result = prediction_result['prediction']
            
            print(f"🤖 ML Prediction: {result} (confidence: {prediction_result.get('confidence', 'N/A')})")
            
        except Exception as e:
            print(f"❌ ML prediction failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"ML prediction failed: {str(e)}"
            )
    else:
        print("❌ ML predictor not ready")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML predictor is not ready"
        )
    
    # Ensure result is in correct format (titlecase)
    if result:
        result = result.title()
        print(f"📝 Final result: {result}")
    
    # Create diagnose data dict with result
    diagnose_dict = {
        "age_on_month": diagnose_data.age_on_month,
        "gender": diagnose_data.gender,
        "height": diagnose_data.height,
        "result": result
    }
    
    # Create the diagnose history with result
    diagnose = create_diagnose_history(db, diagnose_dict, children_id)
    
    return diagnose


@router.get("/{children_id}/diagnose/{diagnose_id}/report")
def generate_diagnose_report(
    children_id: int,
    diagnose_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate PDF report for specific diagnose (Admin only)"""
    # Check if user is admin
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required to generate reports."
        )
    
    try:
        # Verify children belongs to current user
        children = get_children_by_id(db, children_id, current_user.id)
        if not children:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Children not found"
            )
        
        # Verify diagnose exists and belongs to the children
        diagnose = get_diagnose_history_by_id(db, diagnose_id, children_id)
        if not diagnose:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diagnose not found"
            )
        
        # Generate PDF report
        pdf_filepath = pdf_service.generate_diagnose_report(
            db=db,
            diagnose_id=diagnose_id,
            children_id=children_id,
            user_id=current_user.id
        )
        
        # Generate download URL
        download_url = pdf_service.get_report_url(pdf_filepath)
        
        return {
            "message": "PDF report generated successfully",
            "download_url": download_url,
            "filename": pdf_filepath.split("/")[-1],
            "diagnose_id": diagnose_id,
            "children_id": children_id
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        print(f"❌ Error generating PDF report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate PDF report: {str(e)}"
        )


@router.get("/{children_id}/diagnose", response_model=List[DiagnoseHistoryResponse])
def get_diagnose_list(
    children_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all diagnose histories for specific children"""
    try:
        # Verify children belongs to current user
        children = get_children_by_id(db, children_id, current_user.id)
        if not children:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Children not found"
            )
        
        diagnose_histories = get_diagnose_histories_by_children(db, children_id)
        print(f"📊 Found {len(diagnose_histories)} diagnose histories for children {children_id}")
        return diagnose_histories
        
    except Exception as e:
        print(f"❌ Error in get_diagnose_list: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/predictor/status")
def get_predictor_status():
    """Get the status of the stunting predictor"""
    from app.predictor import is_predictor_ready, get_predictor
    
    if is_predictor_ready():
        predictor = get_predictor()
        cache_status = predictor.cache_status()
        model_info = predictor.get_model_info()
        
        return {
            "status": "ready",
            "model_info": model_info,
            "cache_status": cache_status
        }
    else:
        return {
            "status": "not_ready",
            "message": "Stunting predictor is not initialized or trained"
        }


@router.get("/{children_id}/diagnose/{diagnose_id}", response_model=DiagnoseHistoryResponse)
def get_diagnose_detail(
    children_id: int,
    diagnose_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific diagnose detail"""
    # Verify children belongs to current user
    children = get_children_by_id(db, children_id, current_user.id)
    if not children:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Children not found"
        )
    
    diagnose = get_diagnose_history_by_id(db, diagnose_id, children_id)
    if not diagnose:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnose not found"
        )
    
    return diagnose
