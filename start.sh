#!/usr/bin/env bash
# English Seekho — Startup Script (Linux / Mac)

set -e

echo ""
echo "🎓 English Seekho — English Learning Chatbot"
echo "============================================="
echo ""

# Navigate to backend
cd "$(dirname "$0")/backend"

# Install requirements if needed
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt --quiet

# Download NLTK data (skips if already present)
echo "📥 Checking NLTK data..."
python3 -c "
import nltk
for pkg in ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger', 'punkt_tab']:
    try:
        nltk.data.find(f'tokenizers/{pkg}' if 'punkt' in pkg else f'corpora/{pkg}')
        print(f'  ✓ {pkg} already downloaded')
    except LookupError:
        print(f'  ↓ Downloading {pkg}...')
        nltk.download(pkg, quiet=True)
"

echo ""
echo "✅ Ready! Opening frontend..."
echo ""

# Open the frontend in default browser (background)
FRONTEND="$(dirname "$0")/frontend/index.html"

if command -v xdg-open &>/dev/null; then
    xdg-open "$FRONTEND" &
elif command -v open &>/dev/null; then
    open "$FRONTEND" &
fi

echo "🌐 Frontend: file://$FRONTEND"
echo "🔌 Backend:  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server."
echo ""

# Start Flask
python3 app.py
