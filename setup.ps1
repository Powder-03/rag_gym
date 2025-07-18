# Install dependencies
Write-Host "Installing Python dependencies..." -ForegroundColor Green
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Green
    Copy-Item ".env.example" ".env"
    Write-Host "Please edit .env file and add your Google API key" -ForegroundColor Yellow
    Write-Host "Get your API key from: https://makersuite.google.com/app/apikey" -ForegroundColor Cyan
} else {
    Write-Host ".env file already exists" -ForegroundColor Blue
}

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start the application, you have several options:" -ForegroundColor Cyan
Write-Host "1. Full Stack (Recommended): .\start_app.bat" -ForegroundColor White
Write-Host "2. Backend Only: python main.py" -ForegroundColor White  
Write-Host "3. Frontend Only: .\run_streamlit.bat" -ForegroundColor White
Write-Host "4. Docker: docker-compose up --build" -ForegroundColor White
Write-Host ""
Write-Host "Access Points:" -ForegroundColor Yellow
Write-Host "• Streamlit Frontend: http://localhost:8501" -ForegroundColor Green
Write-Host "• FastAPI Backend: http://localhost:8001" -ForegroundColor Green
Write-Host "• API Documentation: http://localhost:8001/docs" -ForegroundColor Green
