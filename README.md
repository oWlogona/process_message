# FastAPI Text Processing API

## Project Description

This FastAPI application provides a text processing API that allows users to submit text for processing and receive results. It supports various text types, including chat items, summaries, and articles, each with specific length limits. The processed texts are published to a RabbitMQ queue for further handling. Processing results are stored in a database and can be retrieved using a task ID.

## Features

- Process texts with different types (`chat_item`, `summary`, `article`).
- Validate text length based on its type.
- Store processing results and retrieve them using a task ID.
- Use RabbitMQ for task processing and message queuing.
- Support asynchronous message consumption through a worker.

## Project Structure

```bash
genesis
- app/
  -- __init__.py          # Module initialization
  -- main.py              # Main FastAPI application entry point
  -- worker.py            # Worker for consuming messages from RabbitMQ
  -- tasks.py             # Task logic for text processing
  -- db.py                # Database configuration and models
  - api/
    -- __init__.py        # API module initialization
    -- endpoints.py       # API endpoints for text processing
  - services/
    -- rabbit/
       -- connection.py   # RabbitMQ connection logic
    -- storage/
       -- models.py       # Database models
       -- database.py     # Database interaction logic
  - logic/
    -- consumer.py        # Logic for consuming messages from RabbitMQ
  - common/
    -- tasks.py           # Common logic for text processing tasks
- docker-compose.yml      # Docker Compose configuration for app and RabbitMQ
- Dockerfile              # Dockerfile for building the application image
- .env                    # Environment variables configuration
```

## Setup Instructions

### Prerequisites

- Python 3.12 or higher
- RabbitMQ
- PostgreSQL (if using a database for storage)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

## Run with Docker

The project includes a `docker-compose.yml` file, allowing you to easily run the application along with RabbitMQ:

```bash
docker-compose up --build
```

### This command will start three services:

- app: The main FastAPI application.
- rabbit: RabbitMQ message broker.
- worker: A worker that consumes messages from RabbitMQ.

## 2. Submit Text for Processing

### Request

**Endpoint:** `POST /process-text`

**Example Request:**

```json
{
  "type": "chat_item",
  "text": "Hey! Just wanted to confirm if we're still meeting for lunch tomorrow."
}
```

### Parameters:
- text (str): The text to be processed.
- type (str): The type of the text (chat_item, summary, article).

### 3. Retrieve Processing Result

```bash
GET /task/{task_id}
```

Returns the result of the text processing for the given task ID.
```json
{
  "task_id": "a8e0e44a-07d7-407e-8b79-4bcd1691f9cb",
  "original_text": "Hey!/// Just wanted to confirm if we're still meeting for lunch tomorrow at 12 pm.",
  "processed_text": "Hey! Just wanted to confirm if we're still meeting for lunch tomorrow at 12 pm.",
  "type": "chat_item",
  "word_count": 15,
  "language": "en",
  "status": "completed"
}
```