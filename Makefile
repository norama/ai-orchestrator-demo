dev-be:
	cd backend && poetry run uvicorn app.main:app --reload --host 127.0.0.1

dev-debug-be:
	cd backend && poetry run debugpy --listen 5678 -m uvicorn app.main:app --reload --no-access-log

test-be:
	cd backend && poetry run pytest -v

dev-fe:
	cd frontend && npm run dev -- --host 127.0.0.1
