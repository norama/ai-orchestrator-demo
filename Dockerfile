# ===============================
# 1) Frontend build stage
# ===============================
FROM node:20-slim AS frontend-build

WORKDIR /build/frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend .
RUN npm run build


# ===============================
# 2) Backend runtime stage
# ===============================
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /srv

# install poetry
RUN pip install --no-cache-dir poetry

# install backend deps
COPY backend/pyproject.toml backend/poetry.lock ./backend/
RUN cd backend \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# copy backend code
COPY backend ./backend

# copy frontend build output
COPY --from=frontend-build /build/frontend/dist ./frontend

# run backend
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
