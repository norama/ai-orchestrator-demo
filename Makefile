dev-be:
	cd backend && poetry run uvicorn app.main:app --reload --host 127.0.0.1

dev-fe:
	cd frontend && npm run dev -- --host 127.0.0.1
