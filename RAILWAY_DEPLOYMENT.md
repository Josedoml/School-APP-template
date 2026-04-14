# 🚀 Railway Deployment Guide

## Prerequisites
- Docker image tested and working locally ✅
- Railway account and API token
- GitHub repository (optional, can deploy from Docker image)

## Deployment Options

### Option 1: Direct Docker Image Deployment
```bash
# Push image to Docker Hub
docker tag school-management-prod:latest YOUR_DOCKER_USERNAME/school-management:latest
docker push YOUR_DOCKER_USERNAME/school-management:latest

# In Railway Dashboard:
# 1. Create new project
# 2. Add from Docker image
# 3. Paste image: YOUR_DOCKER_USERNAME/school-management:latest
# 4. Set environment variables
```

### Option 2: GitHub + Railway (Recommended)
```bash
# 1. Create GitHub repository
# 2. Push code
git remote add origin https://github.com/YOUR_USERNAME/school-management.git
git push -u origin main

# 3. In Railway Dashboard:
#    - Create new project
#    - Connect GitHub
#    - Select school-management repo
#    - Railway auto-detects Dockerfile
#    - Set environment variables
```

## Environment Variables on Railway

Set these in Railway Project Settings:

```
PORT=8000
DATABASE_URL=postgresql://user:password@host:port/school
SECRET_KEY=your-super-secret-key-here-change-in-production
```

## Using Railway PostgreSQL Plugin

1. In Railway project, click "Add"
2. Select "PostgreSQL"
3. Copy connection string to DATABASE_URL
4. Railway will auto-inject required vars

## Deploy Command (If Using Railway CLI)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login --token fff5a045-b334-4016-994e-b6a2da2a0eb2

# Initialize project
cd /Users/pepelucho90/ai-system/workspace
railway init --name school-management

# Add PostgreSQL (optional)
railway add --plugin postgresql

# Deploy
railway up
```

## Access Your App

After deployment:
```bash
railway open
```

Or visit: `https://your-project-name.railway.app`

## Testing the App

1. Open login page: `https://your-domain/`
2. Register new account (choose: student, teacher, or admin)
3. Login with credentials
4. Access dashboard with tabs:
   - Dashboard (analytics & charts)
   - Grades (view/add student grades)
   - Attendance (mark attendance)
   - Messages (send/receive messages)
   - Calendar (manage events)

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login with username/password

### Grades
- `GET /grades/{student_id}` - Get grades for student
- `POST /grades` - Add grade (requires auth token)

### Attendance  
- `GET /attendance/{student_id}` - Get attendance records
- `POST /attendance` - Mark attendance (requires auth token)

### Messages
- `GET /messages` - Get all messages for user
- `POST /messages` - Send message (requires auth token)

### Calendar
- `GET /calendar` - Get calendar events for user
- `POST /calendar` - Create event (requires auth token)

### Health
- `GET /health` - Health check endpoint

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run app
python main.py

# Visit http://localhost:8000
```

## Troubleshooting

**App won't start:**
```bash
railway logs
```

**Database connection error:**
- Verify DATABASE_URL format
- Check PostgreSQL is running
- Confirm credentials are correct

**Port conflicts:**
- Railway uses environment variable PORT
- App automatically reads PORT env var

**CORS issues:**
- CORS is enabled for all origins (*)
- Modify in main.py if needed for security

## Next Steps

1. Push code to GitHub
2. Connect GitHub to Railway
3. Set environment variables
4. Deploy
5. Access public URL
6. Share with school administrators

## Support

For issues:
- Check Railway logs: `railway logs`
- Verify environment variables
- Ensure database migrations ran
- Check network connectivity

---

**Local Access:** http://localhost:8000
**Production:** `https://your-domain.railway.app` (after deployment)
