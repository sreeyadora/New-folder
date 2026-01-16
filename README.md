📧 ReachInbox – Email Scheduler (Full Stack Assignment)
📌 Overview

ReachInbox Email Scheduler is a full-stack web application that allows users to:

Authenticate securely

Schedule emails for future delivery

View scheduled and sent emails

Handle background email processing using a queue system

This project demonstrates frontend + backend integration, authentication flow, background workers, and database usage.
📧 ReachInbox – Email Scheduler (Full Stack Assignment)
📌 Overview

ReachInbox Email Scheduler is a full-stack web application that allows users to:

Authenticate securely

Schedule emails for future delivery

View scheduled and sent emails

Handle background email processing using a queue system

This project demonstrates frontend + backend integration, authentication flow, background workers, and database usage.
email-scheduler/
## Project Structure

```text
email-scheduler/
├── backend/
│   ├── server.py
│   ├── config.py
│   ├── celery_app.py
│   ├── requirements.txt
│   ├── .env
│   └── tasks/
│       └── email_tasks.py
│
├── frontend/
│   ├── package.json
│   ├── .env
│   ├── public/
│   └── src/
│       ├── App.js
│       ├── pages/
│       │   ├── LoginPage.js
│       │   ├── LoginCallback.js
│       │   └── UserDashboard.js
│       └── components/
│           └── EmailComposer.js
│
└── README.md
```

🚀 Features Implemented
✅ Authentication

Google OAuth login flow

Secure session handling using cookies

Protected routes on frontend

✅ Dashboard

Displays logged-in user details

Personalized greeting

Simple and clean UI

✅ Email Scheduling

Compose new email

Schedule email with delay

View scheduled emails

View sent emails

✅ Background Processing

Celery worker handles email sending

Redis used as task queue

MongoDB stores jobs and logs

⚙️ Setup Instructions
1️⃣ Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt

Create .env file:

MONGO_URL=mongodb://localhost:27017
DB_NAME=email_scheduler_db
REDIS_URL=redis://localhost:6379/0
ETHEREAL_SMTP_HOST=smtp.ethereal.email
ETHEREAL_SMTP_PORT=587
ETHEREAL_SMTP_USER=your_ethereal_email
ETHEREAL_SMTP_PASSWORD=your_password

Run backend:

uvicorn server:app --reload --port 8001


Start Celery worker:

celery -A celery_app worker --loglevel=info

2️⃣ Frontend Setup
cd frontend
npm install
npm start


Create .env:
REACT_APP_BACKEND_URL=http://localhost:8001

🔍 How to Use

Open http://localhost:3000

Login using Google

Access dashboard

Compose and schedule emails

View scheduled and sent emails

Emails are captured using Ethereal (test SMTP)

🧪 Testing Notes

Emails are not sent to real inboxes

Ethereal Email is used for safe testing

All backend APIs can be tested via:

http://localhost:8001/docs

🧠 Design Decisions

UI intentionally kept simple for clarity

Clear separation between frontend and backend

Background jobs used to avoid blocking API

Focus on correctness over excessive UI polish

⚠️ Known Limitations

No real production SMTP

No advanced retry UI

Minimal styling (intentional for assignment)

📌 Conclusion

This project demonstrates:

Full-stack development skills

API design and integration

Background job processing

Authentication flow

Practical software architecture

📸 Screenshots

Below are screenshots demonstrating the core functionality of the Email Scheduler application.

🔐 Login Page

Shows Google authentication entry point for users.
![alt text](image.png)
![alt text](image-1.png)
![alt text](image-4.png)
![alt text](image-5.png)



🏠 Dashboard

Displays logged-in user details and navigation to email actions.
![alt text](image-3.png)



✉️ Compose Email

Allows users to compose and schedule emails with recipient, subject, body, and timing.
![alt text](image-6.png)


⏳ Scheduled Emails

Shows all emails that are queued and scheduled to be sent.
![alt text](image-7.png)


✅ Sent Emails

Displays emails that have already been delivered along with their status.
![alt text](image-8.png)

👤 Author

Sreeya Dora
Email: sreeya.dr@gmail.com
