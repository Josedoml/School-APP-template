#!/bin/bash

# Railway Deployment Script
# This script helps deploy the School Management App to Railway

echo "🚀 School Management System - Railway Deployment"
echo "=================================================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    curl -o railway-cli.sh https://releases.railway.app/railway.sh
    chmod +x railway-cli.sh
    ./railway-cli.sh
fi

echo "✅ Authenticating with Railway..."
railway login --token "fff5a045-b334-4016-994e-b6a2da2a0eb2"

echo "✅ Initializing Railway project..."
railway init --name "school-management"

echo "✅ Adding PostgreSQL plugin..."
railway add --plugin postgresql

echo "✅ Setting environment variables..."
railway variables set SECRET_KEY="your-secure-key-here-change-in-production"
railway variables set PORT=8000

echo "✅ Deploying application..."
railway up

echo ""
echo "✅ Deployment complete!"
echo "📍 Your app is now live on Railway!"
echo ""
echo "To view your app:"
echo "  railway open"
echo ""
echo "To view logs:"
echo "  railway logs"
echo ""
echo "To set more variables:"
echo "  railway variables set KEY=VALUE"
