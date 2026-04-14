# School Management System - Development Guide

## Project Structure

```
workspace/
├── main.py                    # FastAPI backend
├── login.html                 # Login/registration page
├── dashboard.html             # Main dashboard interface
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container configuration
├── .dockerignore             # Docker build exclusions
├── railway.json              # Railway deployment config
├── deploy-railway.sh         # Railway deployment script
├── README.md                 # Project overview
└── RAILWAY_DEPLOYMENT.md     # Deployment instructions
```

## Quick Start (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python main.py

# Open browser
http://localhost:8000
```

## Docker Build & Run

```bash
# Build image
docker build -t school-management:latest .

# Run container
docker run -d -p 8000:8000 \
  -e SECRET_KEY="your-secret-key" \
  -e DATABASE_URL="sqlite:///./school.db" \
  --name school-app \
  school-management:latest

# View logs
docker logs school-app

# Stop container
docker stop school-app
docker rm school-app
```

## Architecture

### Backend (FastAPI)
- User authentication (JWT + bcrypt)
- SQLAlchemy ORM for database
- RESTful API endpoints
- CORS enabled for frontend

### Database Models
- **User** - Registration, login, roles
- **Student** - Student profiles
- **Grade** - Subject grades by semester
- **Attendance** - Daily attendance records
- **Message** - Inter-user messaging
- **CalendarEvent** - School events and deadlines

### Frontend (HTML/JS)
- Responsive dashboard
- Real-time data visualization (Chart.js)
- Form-based data entry
- JWT token storage (localStorage)
- Role-based UI adjustments

## Key Features

### Authentication
- Register with role selection (student/teacher/admin)
- JWT-based session management
- Password hashing with bcrypt
- Token expiration (24 hours)

### Grade Management
- Track grades by subject and semester
- View grade distribution analytics
- Add/update grades (admin/teacher only)

### Attendance System
- Mark attendance (present/absent/late)
- View attendance history
- Attendance trend analytics
- Real-time status updates

### Messaging
- Send messages between users
- View conversation history
- Timestamp tracking

### Calendar & Agenda
- Create school events
- Multiple event types (assignment/exam/holiday/meeting)
- View upcoming deadlines
- Personal event management

## Environment Variables

```
PORT=8000                              # Server port (Railway auto-sets)
DATABASE_URL=sqlite:///./school.db    # Database connection string
SECRET_KEY=your-secret-key-here       # JWT signing key
```

## API Usage Examples

### Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123",
    "role": "student"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=securepass123"
```

### Add Grade (with auth token)
```bash
curl -X POST http://localhost:8000/grades \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d "student_id=1&subject=Math&grade=95.5&semester=Fall%202024"
```

## Database

### SQLite (Local Development)
- File-based, no setup required
- Location: `./school.db`
- Auto-creates tables on startup

### PostgreSQL (Production)
- Required for Railway deployment
- Connection: `postgresql://user:pass@host:port/school`
- Tables auto-created via SQLAlchemy

## Authentication Flow

1. User registers → Password hashed with bcrypt → User saved to DB
2. User login → Credentials verified → JWT token generated
3. Token stored in browser localStorage
4. Each API request includes `Authorization: Bearer TOKEN` header
5. Server validates token → Extracts user ID → Allows operation

## Frontend State Management

- JWT token: `localStorage.getItem('token')`
- User info: `localStorage.getItem('user')`
- Automatic redirect to login if token missing/invalid

## Development Tips

### Add New Endpoint
```python
@app.post("/api/new-endpoint")
def new_endpoint(param: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Your logic here
    return {"status": "success"}
```

### Add New Model
```python
class NewModel(Base):
    __tablename__ = "new_models"
    id = Column(Integer, primary_key=True)
    # Add columns here
    
Base.metadata.create_all(bind=engine)  # Creates table
```

### Update Dashboard
- Edit `dashboard.html`
- Add new tab in `<div id="tab-name" class="tab">`
- Add JavaScript function to handle data
- Add navigation button to header

## Security Considerations

⚠️ **Before Production:**

1. Change SECRET_KEY to random 32+ character string
2. Enable HTTPS (Railway provides auto SSL)
3. Restrict CORS origins (if known frontend domain)
4. Implement rate limiting
5. Add input validation
6. Use environment variables for secrets
7. Enable HSTS headers
8. Validate and sanitize all user inputs

## Performance Notes

- SQLite suitable for <100 users (local dev)
- PostgreSQL recommended for production
- Add database indexes for frequently queried fields
- Implement caching for grade/attendance reports
- Consider pagination for large datasets

## Monitoring & Debugging

### View Server Logs
```bash
docker logs school-app -f        # Follow logs
docker logs school-app --tail 50 # Last 50 lines
```

### Check Database
```bash
# SQLite inspection
sqlite3 school.db ".tables"
sqlite3 school.db "SELECT * FROM users;"
```

### Test API
```bash
curl http://localhost:8000/health
```

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Port 8000 already in use | `lsof -i :8000` then kill process or use different port |
| Database locked | Stop all processes accessing DB, clear lock files |
| JWT token invalid | Clear localStorage, re-login |
| CORS error | Ensure `allow_origins=["*"]` in FastAPI middleware |
| Static files not found | Ensure login.html and dashboard.html in /app directory |

## Future Enhancements

- [ ] Email notifications for grades/attendance
- [ ] Parent portal (view child's grades)
- [ ] File uploads (documents, assignments)
- [ ] Real-time notifications (WebSocket)
- [ ] Mobile app (React Native)
- [ ] PDF report generation
- [ ] SMS alerts
- [ ] Video conferencing integration
- [ ] Fee payment system
- [ ] Library management

---

**Created:** 2024
**Status:** Production Ready
**License:** MIT
