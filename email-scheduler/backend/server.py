from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, UploadFile, File
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import requests
from celery_app import celery_app
from tasks.email_tasks import send_email_task
import csv
import io

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

# MongoDB connection
mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

# FastAPI app
app = FastAPI(title="Email Scheduler API")
api_router = APIRouter(prefix="/api")

# -------------------- MODELS --------------------

class User(BaseModel):
    user_id: str
    email: str
    name: str
    picture: Optional[str] = None
    created_at: datetime


class SessionExchangeRequest(BaseModel):
    session_id: str


# -------------------- HELPERS --------------------

async def get_current_user(request: Request) -> Optional[dict]:
    """Get current user from session token"""
    session_token = request.cookies.get("session_token")

    if not session_token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            session_token = auth_header.split(" ")[1]

    if not session_token:
        return None

    session = await db.user_sessions.find_one(
        {"session_token": session_token},
        {"_id": 0}
    )

    if not session:
        return None

    expires_at = session["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        return None

    user = await db.users.find_one(
        {"user_id": session["user_id"]},
        {"_id": 0}
    )

    return user


# -------------------- AUTH ROUTES --------------------

@api_router.post("/auth/session")
async def exchange_session(request: SessionExchangeRequest, response: Response):
    """Exchange session_id for user data and create session"""
    try:
        resp = requests.get(
            "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
            headers={"X-Session-ID": request.session_id},
            timeout=10
        )

        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid session")

        data = resp.json()
        user_id = f"user_{uuid.uuid4().hex[:12]}"

        existing_user = await db.users.find_one({"email": data["email"]}, {"_id": 0})
        if existing_user:
            user_id = existing_user["user_id"]
            await db.users.update_one(
                {"user_id": user_id},
                {"$set": {"name": data["name"], "picture": data["picture"]}}
            )
        else:
            await db.users.insert_one({
                "user_id": user_id,
                "email": data["email"],
                "name": data["name"],
                "picture": data["picture"],
                "created_at": datetime.now(timezone.utc)
            })

        session_token = data["session_token"]
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        await db.user_sessions.insert_one({
            "user_id": user_id,
            "session_token": session_token,
            "expires_at": expires_at,
            "created_at": datetime.now(timezone.utc)
        })

        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=True,
            samesite="none",
            path="/"
        )

        user = await db.users.find_one({"user_id": user_id}, {"_id": 0})
        return user

    except Exception as e:
        logging.error(f"Session exchange error: {e}")
        raise HTTPException(status_code=500, detail="Session exchange failed")


@api_router.get("/auth/me")
async def get_me(request: Request):
    """Get current user"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


@api_router.post("/auth/logout")
async def logout(request: Request, response: Response):
    """Logout user"""
    session_token = request.cookies.get("session_token")
    if session_token:
        await db.user_sessions.delete_one({"session_token": session_token})

    response.delete_cookie("session_token", path="/")
    return {"message": "Logged out successfully"}


# -------------------- EMAIL ROUTES --------------------

@api_router.post("/emails/schedule")
async def schedule_emails(
    request: Request,
    recipients: List[str] = None,
    subject: str = None,
    body: str = None,
    start_time: str = None,
    delay_seconds: int = 2,
    hourly_limit: int = 100,
    file: Optional[UploadFile] = File(None)
):
    """Schedule emails to be sent"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    if file:
        content = await file.read()
        csv_data = csv.reader(io.StringIO(content.decode("utf-8")))
        recipients = [row[0].strip() for row in csv_data if row and "@" in row[0]]

    if not recipients:
        raise HTTPException(status_code=400, detail="No recipients provided")

    if not subject or not body:
        raise HTTPException(status_code=400, detail="Subject and body are required")

    schedule_time = datetime.fromisoformat(start_time.replace("Z", "+00:00"))

    jobs_created = []
    for idx, recipient in enumerate(recipients):
        job_id = f"job_{uuid.uuid4().hex[:16]}"
        job_time = schedule_time + timedelta(seconds=delay_seconds * idx)

        await db.email_jobs.insert_one({
            "job_id": job_id,
            "user_id": user["user_id"],
            "recipient": recipient,
            "subject": subject,
            "body": body,
            "schedule_time": job_time,
            "status": "scheduled",
            "hourly_limit": hourly_limit,
            "delay_seconds": delay_seconds,
            "created_at": datetime.now(timezone.utc)
        })

        send_email_task.apply_async(args=[job_id], eta=job_time)
        jobs_created.append(job_id)

    return {
        "message": f"Scheduled {len(jobs_created)} emails",
        "jobs_created": len(jobs_created),
        "job_ids": jobs_created
    }


@api_router.get("/emails/scheduled")
async def get_scheduled_emails(request: Request):
    """Get all scheduled emails"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    jobs = await db.email_jobs.find(
        {"user_id": user["user_id"], "status": {"$in": ["scheduled", "processing", "rate_limited"]}},
        {"_id": 0}
    ).sort("schedule_time", 1).to_list(1000)

    return {"jobs": jobs, "total": len(jobs)}


@api_router.get("/emails/sent")
async def get_sent_emails(request: Request):
    """Get all sent emails"""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    logs = await db.email_logs.find(
        {"user_id": user["user_id"]},
        {"_id": 0}
    ).sort("sent_at", -1).to_list(1000)

    return {"logs": logs, "total": len(logs)}


@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "celery": celery_app.control.inspect().active() is not None
    }


# -------------------- APP SETUP --------------------

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
