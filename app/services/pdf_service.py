"""
PDF Report Service untuk Stunting Checking App
"""

import os
import uuid
from datetime import datetime
from typing import Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from sqlalchemy.orm import Session
from app.models import DiagnoseHistory, Children, User
from app.crud import get_diagnose_history_by_id, get_children_by_id
from app.config import settings


class PDFReportService:
    def __init__(self):
        self.reports_dir = settings.REPORTS_DIR
        self.base_url = settings.BASE_URL
        self.ensure_reports_directory()
    
    def ensure_reports_directory(self):
        """Ensure reports directory exists"""
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def generate_diagnose_report(self, db: Session, diagnose_id: int, children_id: int, user_id: int) -> str:
        """
        Generate PDF report for diagnose
        
        Args:
            db: Database session
            diagnose_id: ID of the diagnose
            children_id: ID of the children
            user_id: ID of the user (for authorization)
            
        Returns:
            str: Path to the generated PDF file
        """
        # Get diagnose data
        diagnose = get_diagnose_history_by_id(db, diagnose_id, children_id)
        if not diagnose:
            raise ValueError("Diagnose not found")
        
        # Get children data
        children = get_children_by_id(db, children_id, user_id)
        if not children:
            raise ValueError("Children not found")
        
        # Get user data
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"diagnose_report_{diagnose_id}_{timestamp}_{uuid.uuid4().hex[:8]}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.black
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.black
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_LEFT,
            textColor=colors.black
        )
        
        # Title
        title = Paragraph("SURAT KETERANGAN HASIL DIAGNOSA", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Report number
        report_number = f"Nomor: {diagnose_id:06d}"
        story.append(Paragraph(report_number, header_style))
        story.append(Spacer(1, 20))
        
        # Patient information
        story.append(Paragraph("Menerangkan bahwa:", normal_style))
        story.append(Spacer(1, 10))
        
        # Patient details
        patient_data = [
            ["1.", "Nama Pasien", ":", children.name],
            ["2.", "Jenis Kelamin", ":", "Laki-laki" if children.gender == "L" else "Perempuan"],
            ["3.", "Alamat", ":", user.address or "Tidak diisi"]
        ]
        
        patient_table = Table(patient_data, colWidths=[0.5*inch, 1.5*inch, 0.3*inch, 3*inch])
        patient_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(patient_table)
        story.append(Spacer(1, 20))
        
        # Examination date
        exam_date = diagnose.diagnosed_at.strftime("%d %B %Y")
        exam_text = f"Telah diperiksa pada tanggal {exam_date} dengan hasil pemeriksaan sebagai berikut:"
        story.append(Paragraph(exam_text, normal_style))
        story.append(Spacer(1, 15))
        
        # Examination data
        story.append(Paragraph("Data Pemeriksaan :", normal_style))
        story.append(Spacer(1, 10))
        
        exam_data = [
            ["1.", "Umur", ":", f"{diagnose.age_on_month} bulan"],
            ["2.", "Berat Badan", ":", "Tidak diukur"],  # Weight not available in current schema
            ["3.", "Tinggi Badan", ":", f"{diagnose.height} cm"]
        ]
        
        exam_table = Table(exam_data, colWidths=[0.5*inch, 1.5*inch, 0.3*inch, 3*inch])
        exam_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(exam_table)
        story.append(Spacer(1, 20))
        
        # Medical diagnosis
        story.append(Paragraph("Diagnosa Medis :", normal_style))
        story.append(Spacer(1, 10))
        
        # Use raw result from ML predictor
        diagnosis_result = diagnose.result
        story.append(Paragraph(diagnosis_result, normal_style))
        story.append(Spacer(1, 30))
        
        # Footer
        footer_text = f"Dokumen ini dibuat secara otomatis pada {datetime.now().strftime('%d %B %Y pukul %H:%M WIB')}"
        story.append(Paragraph(footer_text, ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.grey
        )))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def get_report_url(self, filepath: str) -> str:
        """
        Generate download URL for the report
        
        Args:
            filepath: Path to the PDF file
            
        Returns:
            str: Download URL
        """
        filename = os.path.basename(filepath)
        return f"{self.base_url}/reports/{filename}"


# Global instance
pdf_service = PDFReportService()