import os

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse


from app.database import get_db
from app.models import Job, Certificate
from app.schemas import GenerationRequest
from app.services.certificate import generate_certificate


router = APIRouter(
    prefix="/api/jobs",
    tags=["Jobs"]
)


@router.post("/")
def create_job(
    request: GenerationRequest,
    db: Session = Depends(get_db)
):
    # Create a new job
    job = Job(
        status="PROCESSING",
        total=len(request.recipients)
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # Create generated folder if it doesn't exist
    os.makedirs("generated", exist_ok=True)

    # Process each recipient
    for recipient in request.recipients:

        certificate = Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            status="PENDING"
        )

        db.add(certificate)
        db.commit()
        db.refresh(certificate)

        try:
            file_path = (
                f"generated/"
                f"{job.id}_{certificate.id}.pdf"
            )

            generate_certificate(
                recipient.name,
                request.event_name,
                request.date,
                file_path
            )

            certificate.status = "SUCCESS"
            certificate.file_path = file_path

            job.successful += 1

        except Exception as e:
            certificate.status = "FAILED"
            certificate.error_message = str(e)

            job.failed += 1

        db.commit()

    # Update final job status
    if job.failed == 0:
        job.status = "COMPLETED"
    elif job.successful == 0:
        job.status = "FAILED"
    else:
        job.status = "PARTIALLY_COMPLETED"

    db.commit()

    return {
        "job_id": job.id,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed
    }
    
@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):

    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        return {"message": "Job not found"}

    return {
        "job_id": job.id,
        "status": job.status,
        "total": job.total,
        "successful": job.successful,
        "failed": job.failed
    }
    
@router.get("/{job_id}/certificates")
def get_certificates(
    job_id: int,
    db: Session = Depends(get_db)
):
    certificates = (
        db.query(Certificate)
        .filter(Certificate.job_id == job_id)
        .all()
    )

    return [
        {
            "certificate_id": certificate.id,
            "recipient_name": certificate.recipient_name,
            "recipient_email": certificate.recipient_email,
            "status": certificate.status,
            "file_path": certificate.file_path
        }
        for certificate in certificates
    ]
    

@router.get("/certificate/{certificate_id}")
def get_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = (
        db.query(Certificate)
        .filter(Certificate.id == certificate_id)
        .first()
    )

    if not certificate:
        return {"message": "Certificate not found"}

    if certificate.status != "SUCCESS":
        return {"message": "Certificate was not generated successfully"}

    if not os.path.exists(certificate.file_path):
        return {"message": "Certificate file not found"}

    return FileResponse(
        certificate.file_path,
        media_type="application/pdf",
        filename=f"certificate_{certificate.id}.pdf"
    )