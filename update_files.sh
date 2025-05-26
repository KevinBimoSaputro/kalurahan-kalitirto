#!/bin/bash
# Script untuk update files di repository

echo "🔄 Updating repository with new code..."

# Backup existing files
mkdir -p backup
cp *.py backup/ 2>/dev/null || true

echo "✅ Files backed up to backup/ folder"
echo "📝 Ready to update with new code!"
