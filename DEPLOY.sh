#!/bin/bash

# School Management System - Deploy to Railway
# This script automates the deployment process

set -e

echo "🎓 School Management System - Railway Deployment"
echo "=================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Step 1: Verify Git is initialized
if [ ! -d .git ]; then
    echo "❌ Not a git repository. Initialize with: git init"
    exit 1
fi

echo -e "${BLUE}Step 1: Verifying Git repository...${NC}"
git log --oneline | head -1
echo -e "${GREEN}✅ Git repository verified${NC}"
echo ""

# Step 2: Ensure code is committed
echo -e "${BLUE}Step 2: Checking for uncommitted changes...${NC}"
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️ Uncommitted changes found. Committing..."
    git add -A
    git commit -m "Pre-deployment commit"
fi
echo -e "${GREEN}✅ All changes committed${NC}"
echo ""

# Step 3: Get GitHub repo URL
echo -e "${BLUE}Step 3: GitHub Repository${NC}"
GITHUB_REPO="https://github.com/Josedoml/School-APP-template"
echo "Repository: $GITHUB_REPO"
echo ""
echo "If you haven't pushed yet, run:"
echo "  git remote add origin $GITHUB_REPO"
echo "  git push -u origin main"
echo ""
echo -e "${GREEN}✅ Ready to deploy${NC}"
echo ""

# Step 4: Deployment instructions
echo -e "${BLUE}Step 4: Railway Deployment Instructions${NC}"
echo ""
echo "1. Visit: https://railway.app"
echo "2. Create a new project"
echo "3. Choose deployment method:"
echo "   A) Deploy from GitHub (Recommended)"
echo "      - Connect GitHub"
echo "      - Select: Josedoml/School-APP-template"
echo "   B) Deploy from Docker Image"
echo "      - Docker image: school-management:latest"
echo ""
echo "4. Add PostgreSQL database (optional)"
echo "   - Click 'Add Service'"
echo "   - Select 'PostgreSQL'"
echo ""
echo "5. Set Environment Variables:"
echo "   - PORT: 8000"
echo "   - SECRET_KEY: (generate secure key)"
echo "   - DATABASE_URL: (auto-filled if using PostgreSQL)"
echo ""
echo "6. Click 'Deploy'"
echo ""

# Step 5: Generate secure key
echo -e "${BLUE}Step 5: Generate Secure KEY${NC}"
echo "You can use this generated key for SECRET_KEY:"
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
echo ""

# Step 6: Summary
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}✅ DEPLOYMENT READY${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""
echo "📍 App Details:"
echo "  - GitHub: $GITHUB_REPO"
echo "  - Project: School Management System"
echo "  - Status: Ready for Railway deployment"
echo ""
echo "📝 Next steps:"
echo "  1. Push code: git push -u origin main"
echo "  2. Deploy on Railway.app"
echo "  3. Access public URL"
echo ""
echo "📚 Documentation:"
echo "  - READ: BUILD_SUMMARY.md (this file)"
echo "  - READ: RAILWAY_DEPLOYMENT.md (detailed steps)"
echo "  - READ: DEVELOPMENT.md (development guide)"
echo ""
