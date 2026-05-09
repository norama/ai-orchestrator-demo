dev-be-clean:
	poetry -C backend env remove --all

dev-be-install:
	poetry -C backend install --no-root

dev-be:
	poetry -C backend run uvicorn app.main:app --reload --host 127.0.0.1

dev-debug-be:
	poetry -C backend run debugpy --listen 5678 -m uvicorn app.main:app --reload --no-access-log

test-be:
	poetry -C backend run pytest -v

dev-fe-install:
	cd frontend && npm install

dev-fe:
	cd frontend && npm run dev -- --host 127.0.0.1
