# School Management System

A comprehensive school management application built with FastAPI, featuring student authentication, grade tracking, attendance marking, messaging, and calendar management.

## Features

- **Authentication**: User registration and login with role-based access (student, teacher, admin)
- **Grade Management**: Track and manage student grades by subject and semester
- **Attendance Tracking**: Real-time attendance marking with multiple status options
- **Messaging System**: Internal messaging between users
- **Calendar & Agenda**: Event management with different event types
- **Analytics Dashboard**: Visual representation of grades and attendance trends
- **Web Dashboard**: Responsive UI for managing all school operations

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, SQLite/PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **Deployment**: Docker, Railway
- **Security**: JWT authentication, password hashing with bcrypt

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

Visit `http://localhost:8000` to access the login page.

## Docker

```bash
# Build image
docker build -t school-management:latest .

# Run container
docker run -d -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./school.db \
  -e SECRET_KEY=your-secret-key \
  school-management:latest
```

## Deployment on Railway

1. Push code to GitHub
2. Connect GitHub to Railway
3. Railway will automatically detect the Dockerfile
4. Set environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SECRET_KEY`: JWT secret key
5. Deploy and get public URL

## API Endpoints

- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /grades/{student_id}` - Get student grades
- `POST /grades` - Add grade
- `GET /attendance/{student_id}` - Get attendance records
- `POST /attendance` - Mark attendance
- `GET /messages` - Get messages
- `POST /messages` - Send message
- `GET /calendar` - Get calendar events
- `POST /calendar` - Create event

## Default Credentials

Create accounts through the registration form at `/login.html`.

## License

MIT
