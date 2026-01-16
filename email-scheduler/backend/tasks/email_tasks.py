import asyncio
import logging
from datetime import datetime, timezone

from celery import Task
from motor.motor_asyncio import AsyncIOMotorClient
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from celery_app import celery_app
from config import settings

logger = logging.getLogger(__name__)


class AsyncTask(Task):
    """Run async code inside Celery task"""

    def __call__(self, *args, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self.run(*args, **kwargs))
        finally:
            loop.close()


@celery_app.task(bind=True, base=AsyncTask, max_retries=3)
async def send_email_task(self, job_id: str):
    """
    Celery task to send a single email.
    Handles rate limiting and retries.
    """
    client = None

    try:
        client = AsyncIOMotorClient(settings.MONGO_URL)
        db = client[settings.DB_NAME]

        job = await db.email_jobs.find_one({"job_id": job_id}, {"_id": 0})
        if not job:
            logger.error(f"Job {job_id} not found")
            return {"status": "error", "message": "Job not found"}

        if job["status"] in ["completed", "failed"]:
            return {"status": "skipped", "message": "Already processed"}

        await db.email_jobs.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "processing",
                    "started_at": datetime.now(timezone.utc)
                }
            }
        )

        recipient = job["recipient"]
        subject = job["subject"]
        body = job["body"]

        msg = MIMEMultipart()
        msg["From"] = settings.ETHEREAL_SMTP_USER
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        await aiosmtplib.send(
            msg,
            hostname=settings.ETHEREAL_SMTP_HOST,
            port=settings.ETHEREAL_SMTP_PORT,
            username=settings.ETHEREAL_SMTP_USER,
            password=settings.ETHEREAL_SMTP_PASSWORD,
            start_tls=True
        )

        sent_at = datetime.now(timezone.utc)

        await db.email_logs.insert_one({
            "job_id": job_id,
            "recipient": recipient,
            "subject": subject,
            "status": "sent",
            "sent_at": sent_at
        })

        await db.email_jobs.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "completed",
                    "completed_at": sent_at
                }
            }
        )

        logger.info(f"Email sent for job {job_id}")
        return {"status": "success"}

    except Exception as e:
        logger.error(f"Error sending email for job {job_id}: {e}")
        raise self.retry(exc=e, countdown=60)

    finally:
        if client:
            client.close()
