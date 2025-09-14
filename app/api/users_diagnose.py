"""
API endpoints untuk diagnose management (Admin only)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, DiagnoseHistory
from app.schemas import DiagnoseHistoryResponse, DiagnoseHistoryCreate
from app.middleware import get_admin_user
from app.crud import (
    get_diagnose_by_id_admin,
    get_all_diagnose_histories,
    get_diagnose_histories_by_children_id,
    create_diagnose_history,
    delete_diagnose_history_admin
)
from app.services.pdf_service import PDFReportService

router = APIRouter()

@router.get("/", response_model=List[DiagnoseHistoryResponse])
def get_all_diagnose_histories_endpoint(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get all diagnose histories from all users (Admin only)"""
    diagnoses = get_all_diagnose_histories(db)
    return diagnoses

@router.get("/{diagnose_id}", response_model=DiagnoseHistoryResponse)
def get_diagnose_by_id_endpoint(
    diagnose_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get diagnose by ID (Admin only)"""
    diagnose = get_diagnose_by_id_admin(db, diagnose_id)
    if not diagnose:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnose not found"
        )
    return diagnose

@router.get("/children/{children_id}", response_model=List[DiagnoseHistoryResponse])
def get_diagnose_histories_by_children_id_endpoint(
    children_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get all diagnose histories by children ID (Admin only)"""
    diagnoses = get_diagnose_histories_by_children_id(db, children_id)
    return diagnoses

@router.post("/children/{children_id}", response_model=DiagnoseHistoryResponse)
def create_diagnose_history_endpoint(
    children_id: int,
    diagnose_data: DiagnoseHistoryCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Create diagnose history for any children (Admin only)"""
    diagnose = create_diagnose_history(db, diagnose_data, children_id)
    return diagnose

@router.delete("/{diagnose_id}")
def delete_diagnose_history_endpoint(
    diagnose_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Delete diagnose history by ID (Admin only)"""
    diagnose = get_diagnose_by_id_admin(db, diagnose_id)
    if not diagnose:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnose not found"
        )
    
    delete_diagnose_history_admin(db, diagnose_id)
    return {"message": "Diagnose history deleted successfully"}

@router.get("/children/{children_id}/diagnose/{diagnose_id}/report")
def generate_diagnose_report_endpoint(
    children_id: int,
    diagnose_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Generate PDF report for specific diagnose (Admin only)"""
    try:
        # Get diagnose data
        diagnose = get_diagnose_by_id_admin(db, diagnose_id)
        if not diagnose:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diagnose not found"
            )
        
        # Verify children exists
        from app.crud import get_children_by_id_admin
        children = get_children_by_id_admin(db, children_id)
        if not children:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Children not found"
            )
        
        # Verify diagnose belongs to children
        if diagnose.children_id != children_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Diagnose does not belong to specified children"
            )
        
        # Generate PDF report
        pdf_service = PDFReportService()
        filename = pdf_service.generate_diagnose_report(
            db=db,
            diagnose_id=diagnose_id,
            children_id=children_id,
            user_id=children.user_id  # Get user_id from children
        )
        
        download_url = pdf_service.get_report_url(filename)
        
        return {
            "message": "PDF report generated successfully",
            "download_url": download_url,
            "filename": filename,
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
