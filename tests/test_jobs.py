from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_job():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Python Workshop",
            "date": "2026-10-10",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "test@gmail.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["total"] == 1
    assert data["successful"] == 1
    assert data["failed"] == 0
    
def test_invalid_email():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Python Workshop",
            "date": "2026-10-10",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "wrong-email"
                }
            ]
        }
    )

    assert response.status_code == 422
    
def test_get_job():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Testing Workshop",
            "date": "2026-10-10",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "test2@gmail.com"
                }
            ]
        }
    )

    job_id = response.json()["job_id"]

    response = client.get(f"/api/jobs/{job_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == job_id
    assert data["status"] == "COMPLETED"
    assert data["total"] == 1
    assert data["successful"] == 1
    assert data["failed"] == 0
    
def test_get_certificates():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Testing Workshop",
            "date": "2026-10-10",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "test3@gmail.com"
                }
            ]
        }
    )

    job_id = response.json()["job_id"]

    response = client.get(
        f"/api/jobs/{job_id}/certificates"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["recipient_name"] == "Test User"
    assert data[0]["status"] == "SUCCESS"
    
def test_get_certificate():
    response = client.post(
        "/api/jobs/",
        json={
            "event_name": "Testing Workshop",
            "date": "2026-10-10",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "test4@gmail.com"
                }
            ]
        }
    )

    job_id = response.json()["job_id"]

    response = client.get(
        f"/api/jobs/{job_id}/certificates"
    )

    certificate_id = response.json()[0]["certificate_id"]

    response = client.get(
        f"/api/jobs/certificate/{certificate_id}"
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"