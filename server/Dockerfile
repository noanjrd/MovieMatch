FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server/ ./server/

WORKDIR /app/server

ARG TMDB_API_KEY
ARG FRONT_URL
ENV TMDB_API_KEY=$TMDB_API_KEY
ENV FRONT_URL=$FRONT_URL

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]