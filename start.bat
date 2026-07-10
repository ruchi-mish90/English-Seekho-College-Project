@echo off
echo.
echo  English Seekho — English Learning Chatbot
echo  ==========================================
echo.

cd /d "%~dp0backend"

echo  Installing Python dependencies...
pip install -r requirements.txt --quiet

echo  Checking NLTK data...
python -c "import nltk; [nltk.download(p, quiet=True) for p in ['punkt','stopwords','wordnet','averaged_perceptron_tagger','punkt_tab']]"

echo.
echo  Opening the chatbot frontend in your browser...
start "" "%~dp0frontend\index.html"

echo.
echo  Backend running at http://localhost:5000
echo  Press Ctrl+C to stop.
echo.

python app.py
pause
