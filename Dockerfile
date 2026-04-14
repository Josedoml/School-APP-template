FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY login.html .
COPY dashboard.html .

EXPOSE 8000

ENV PORT=8000
ENV DATABASE_URL=sqlite:///./school.db
ENV SECRET_KEY=your-secret-key-change-in-production

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
