```
(.venv) Artems-MacBook-Pro-2:hw3 agarkov$ curl -X POST http://localhost:5001/predict -H "Content-Type: application/json" -d '{"text": "I love this project!"}'
{
  "score": 0.9998873472213745,
  "sentiment": "POSITIVE"
}
```

# Sentiment Analysis API with Flask and PostgreSQL

Создаем API, использую Flask и Hugging Face модель. API принимает текст через запрос POST и возвращает значение sentiment (положительное или отрицательное) вместе с оценкой уверенности.
Все запросы и ответы регистрируются в базе данных PostgreSQL.

## Features

- **Sentiment Analysis**: Использует предварительно обученную модель из Hugging Face для анализа текста.
- **API Endpoints**:
  - `/predict`: POST endpoint для отправки текста для sentiment analysis.
  - `/health`: GET health check.
- **PostgreSQL Database**: БД логгирует input, сентимент и confidence score.

### 1. Склонировать репозиторий

```bash
git clone https://github.com/agarkovv/system-design-sbt
git checkout hw3
cd hw3
```

### 2. Build and Run

```bash
docker-compose up --build
```

- Билдим Flask app
- Билдим БД
- Разворачиваем оба сервиса и свзяываем их друг с другом

### 3. Доступ по API

API URL: http://localhost:5001

**Пример**:

```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text": "I love this!"}'
{
"sentiment": "POSITIVE",
"score": 0.9998
}
```

### 4. Database Logs

```bash
docker exec -it sentiment_db psql -U postgres -d sentiment_db
SELECT \* FROM logs;
```

### 5. Остановка

```bash
docker-compose down
```