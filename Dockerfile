FROM node:20.19.0-bookworm-slim AS frontend-build
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./frontend/
RUN cd frontend && npm install
COPY frontend ./frontend
RUN cd frontend && npm run build

FROM python:3.12.6-slim-bookworm
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist
RUN mkdir -p app/static && cp -r frontend/dist/* app/static/
ENV PORT=5001
EXPOSE 5001
CMD ["sh", "-c", "gunicorn wsgi:app --bind 0.0.0.0:${PORT}"]
