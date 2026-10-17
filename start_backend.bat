@echo off
cd /d "D:\project data\AI_afforestation"
"D:\project data\AI_afforestation\ai_env\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2