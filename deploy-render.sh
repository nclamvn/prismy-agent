#!/bin/bash
echo "🚀 Deploying to Render..."

# Ensure git is clean
git add .
git commit -m "Prepare for Render deployment"
git push origin main

echo "✅ Code pushed to GitHub"
echo "📝 Next steps:"
echo "1. Go to https://render.com"
echo "2. Connect GitHub repo"
echo "3. Use render.yaml for auto-setup"
echo "4. Add environment variables in dashboard"
