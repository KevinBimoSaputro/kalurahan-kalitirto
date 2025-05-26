#!/bin/bash

echo "🚀 Deploying Feedback System..."

# Generate ML models
echo "📊 Generating ML models..."
python create_models.py

# Git operations
echo "📦 Preparing for deployment..."
git add .
git commit -m "🎉 Deploy: Complete feedback system with ML models"
git push origin main

echo "✅ Deployment complete!"
echo "🌐 Now deploy to Streamlit Cloud:"
echo "   1. Go to share.streamlit.io"
echo "   2. Connect your repository"
echo "   3. Set main file: app.py"
echo "   4. Add secrets from .streamlit/secrets.toml"
echo "   5. Deploy!"
