from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime, timedelta
from typing import List, Optional
import os
from passlib.context import CryptContext
from jose import JWTError, jwt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets

# Database Setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./school.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"

# Email Configuration
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@schoolmanagement.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="student")
    is_active = Column(Boolean, default=True)
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    student_id = Column(String, unique=True)
    grade_level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject = Column(String)
    grade = Column(Float)
    semester = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(DateTime)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    recipient_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class CalendarEvent(Base):
    __tablename__ = "calendar_events"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    event_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Pydantic Schemas with ORM mode
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "student"

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class GradeResponse(BaseModel):
    id: int
    subject: str
    grade: float
    semester: str
    model_config = ConfigDict(from_attributes=True)

class AttendanceResponse(BaseModel):
    id: int
    date: datetime
    status: str
    model_config = ConfigDict(from_attributes=True)

class MessageCreate(BaseModel):
    recipient_id: int
    content: str

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    recipient_id: int
    content: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class CalendarEventCreate(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    event_type: str

class CalendarEventResponse(BaseModel):
    id: int
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    event_type: str
    model_config = ConfigDict(from_attributes=True)

# Email Service
def send_email(to_email: str, subject: str, body: str, html_body: str = None):
    """Send email via SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = to_email
        
        msg.attach(MIMEText(body, 'plain'))
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def send_password_reset_email(email: str, reset_token: str):
    """Send password reset email"""
    reset_url = f"{FRONTEND_URL}/reset-password.html?token={reset_token}"
    
    subject = "School Management System - Password Reset Request"
    
    text_body = f"""
    Hello,
    
    You requested a password reset for your School Management System account.
    
    Click the link below to reset your password (valid for 1 hour):
    {reset_url}
    
    If you didn't request this, please ignore this email.
    
    Best regards,
    School Management System Team
    """
    
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: 0 auto;">
                <h2 style="color: #011f5b;">Password Reset Request</h2>
                <p>Hello,</p>
                <p>You requested a password reset for your School Management System account.</p>
                <p>Click the button below to reset your password (valid for 1 hour):</p>
                <p>
                    <a href="{reset_url}" style="background-color: #0066cc; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">
                        Reset Password
                    </a>
                </p>
                <p>Or copy this link: <a href="{reset_url}">{reset_url}</a></p>
                <p style="color: #666; font-size: 12px;">If you didn't request this, please ignore this email.</p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="color: #999; font-size: 12px;">School Management System Team</p>
            </div>
        </body>
    </html>
    """
    
    return send_email(email, subject, text_body, html_body)

# FastAPI App
app = FastAPI(title="School Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Auth Endpoints
@app.post("/auth/register", response_model=AuthResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    access_token = create_access_token(data={"sub": db_user.id})
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(db_user)
    )

@app.post("/auth/login", response_model=AuthResponse)
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.id})
    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.from_orm(user)
    )

@app.post("/auth/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        # Don't reveal if email exists (security best practice)
        return {"message": "If email exists, password reset link has been sent"}
    
    # Generate reset token (valid for 1 hour)
    reset_token = secrets.token_urlsafe(32)
    reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    
    user.reset_token = reset_token
    user.reset_token_expires = reset_token_expires
    db.commit()
    
    # Send email
    email_sent = send_password_reset_email(user.email, reset_token)
    
    if not email_sent:
        raise HTTPException(status_code=500, detail="Failed to send reset email. Please try again later.")
    
    return {"message": "Password reset link has been sent to your email"}

@app.post("/auth/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == request.token).first()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid reset token")
    
    # Check if token has expired
    if user.reset_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Reset token has expired. Please request a new one.")
    
    # Update password
    user.hashed_password = hash_password(request.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    
    return {"message": "Password has been reset successfully"}

@app.post("/auth/verify-reset-token")
def verify_reset_token(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.reset_token == token).first()
    
    if not user:
        return {"valid": False, "message": "Invalid reset token"}
    
    if user.reset_token_expires < datetime.utcnow():
        return {"valid": False, "message": "Reset token has expired"}
    
    return {"valid": True, "message": "Token is valid"}

# Grades Endpoints
@app.get("/grades/{student_id}")
def get_grades(student_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    grades = db.query(Grade).filter(Grade.student_id == student_id).all()
    return [GradeResponse.from_orm(g) for g in grades]

@app.post("/grades")
def add_grade(student_id: int, subject: str, grade: float, semester: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_grade = Grade(student_id=student_id, subject=subject, grade=grade, semester=semester)
    db.add(db_grade)
    db.commit()
    return {"status": "Grade added"}

# Attendance Endpoints
@app.get("/attendance/{student_id}")
def get_attendance(student_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    attendance = db.query(Attendance).filter(Attendance.student_id == student_id).all()
    return [AttendanceResponse.from_orm(a) for a in attendance]

@app.post("/attendance")
def update_attendance(student_id: int, status: str, date: datetime, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_attendance = Attendance(student_id=student_id, status=status, date=date)
    db.add(db_attendance)
    db.commit()
    return {"status": "Attendance updated"}

# Messages Endpoints
@app.get("/messages")
def get_messages(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    messages = db.query(Message).filter((Message.recipient_id == current_user.id) | (Message.sender_id == current_user.id)).all()
    return [MessageResponse.from_orm(m) for m in messages]

@app.post("/messages")
def send_message(msg: MessageCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_message = Message(sender_id=current_user.id, recipient_id=msg.recipient_id, content=msg.content)
    db.add(db_message)
    db.commit()
    return {"status": "Message sent"}

# Calendar Endpoints
@app.get("/calendar")
def get_calendar(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    events = db.query(CalendarEvent).filter(CalendarEvent.user_id == current_user.id).all()
    return [CalendarEventResponse.from_orm(e) for e in events]

@app.post("/calendar")
def create_event(event: CalendarEventCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_event = CalendarEvent(user_id=current_user.id, **event.dict())
    db.add(db_event)
    db.commit()
    return {"status": "Event created"}

# Health Check
@app.get("/health")
def health_check():
    return {"status": "running"}

# Serve static files
@app.get("/")
async def root():
    return FileResponse("login.html", media_type="text/html")

@app.get("/login.html")
async def get_login():
    return FileResponse("login.html", media_type="text/html")

@app.get("/dashboard.html")
async def get_dashboard():
    return FileResponse("dashboard.html", media_type="text/html")

@app.get("/forgot-password.html")
async def get_forgot_password():
    return FileResponse("forgot-password.html", media_type="text/html")

@app.get("/reset-password.html")
async def get_reset_password():
    return FileResponse("reset-password.html", media_type="text/html")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
