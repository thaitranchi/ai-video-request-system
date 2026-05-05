# scripts/run_backend.sh
source venv/Scripts/activate
uvicorn app.main:app --reload --app-dir backend