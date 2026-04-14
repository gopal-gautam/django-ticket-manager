# Django IT Ticket Manager API

A beginner-friendly Django REST API project for managing IT support tickets. This project is designed to be dockerized with PostgreSQL and Redis, making it perfect for learning Docker Compose with Django.

## 📋 Features

- ✅ Full CRUD operations for support tickets
- ✅ PostgreSQL database for persistent storage
- ✅ Redis caching for improved API performance
- ✅ Docker Compose setup for easy deployment
- ✅ Gunicorn production WSGI server
- ✅ Health check endpoint for monitoring
- ✅ Environment variable configuration
- ✅ Django REST Framework for API development

## 📁 Project Structure

```
django-ticket-manager/
├── config/                  # Django project configuration
│   ├── __init__.py
│   ├── settings.py          # Main settings (DB, Redis, etc.)
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── tickets/                 # Main Django app for ticket management
│   ├── __init__.py
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Ticket data model
│   ├── serializers.py       # DRF serializers
│   ├── urls.py              # App URL patterns
│   └── views.py             # API view logic
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Multi-container orchestration
├── entrypoint.sh            # Container startup script
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── manage.py                # Django management script
└── README.md                # This file
```

## 🚀 Quick Start with Docker Compose

### Prerequisites

- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd django-ticket-manager
```

### Step 2: Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your preferred values (optional - defaults work for development)
```

### Step 3: Build and Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

This will:
1. Build the Django Docker image
2. Start a PostgreSQL container
3. Start a Redis container
4. Run database migrations
5. Start the Django API with Gunicorn on port 8000

### Step 4: Access the API

The API is now running at: `http://localhost:8000`

- **API Endpoints**: `http://localhost:8000/api/tickets/`
- **Health Check**: `http://localhost:8000/api/health/`
- **Django Admin**: `http://localhost:8000/admin/`

## 🧪 Testing the API with cURL

### 1. Health Check

```bash
curl -X GET http://localhost:8000/api/health/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Django Ticket Manager API",
  "database": "connected",
  "redis": "connected"
}
```

### 2. Create a New Ticket

```bash
curl -X POST http://localhost:8000/api/tickets/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cannot access email",
    "description": "I am unable to access my company email since this morning. Getting authentication error.",
    "status": "open",
    "priority": "high",
    "requester_name": "John Doe",
    "requester_email": "john.doe@example.com"
  }'
```

**Expected Response:**
```json
{
  "id": 1,
  "title": "Cannot access email",
  "description": "I am unable to access my company email since this morning. Getting authentication error.",
  "status": "open",
  "priority": "high",
  "requester_name": "John Doe",
  "requester_email": "john.doe@example.com",
  "created_at": "2026-04-14T10:30:00Z",
  "updated_at": "2026-04-14T10:30:00Z"
}
```

### 3. List All Tickets

```bash
curl -X GET http://localhost:8000/api/tickets/
```

**Expected Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Cannot access email",
      "description": "I am unable to access my company email since this morning.",
      "status": "open",
      "priority": "high",
      "requester_name": "John Doe",
      "requester_email": "john.doe@example.com",
      "created_at": "2026-04-14T10:30:00Z",
      "updated_at": "2026-04-14T10:30:00Z"
    }
  ]
}
```

### 4. Retrieve a Single Ticket

```bash
curl -X GET http://localhost:8000/api/tickets/1/
```

### 5. Update a Ticket (Full Update - PUT)

```bash
curl -X PUT http://localhost:8000/api/tickets/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cannot access email - Updated",
    "description": "I am unable to access my company email. Issue persists.",
    "status": "in_progress",
    "priority": "high",
    "requester_name": "John Doe",
    "requester_email": "john.doe@example.com"
  }'
```

### 6. Partially Update a Ticket (PATCH) - Change Status Only

```bash
# Update ticket status to resolved
curl -X PATCH http://localhost:8000/api/tickets/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved"
  }'

# Update ticket priority only
curl -X PATCH http://localhost:8000/api/tickets/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "priority": "critical"
  }'
```

### 7. Delete a Ticket

```bash
curl -X DELETE http://localhost:8000/api/tickets/1/
```

**Expected Response:** `204 No Content` (empty response)

## 🛠️ Local Development (Without Docker)

If you want to run the project locally without Docker:

### Step 1: Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### Step 2: Set Up PostgreSQL

Make sure you have PostgreSQL installed and running. Create a database:

```bash
createdb ticket_manager
```

### Step 3: Set Up Redis

Make sure Redis is installed and running on your system.

### Step 4: Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your local PostgreSQL credentials.

### Step 5: Run Migrations

```bash
uv run python manage.py migrate
```

### Step 6: Create Superuser (Optional - for admin access)

```bash
uv run python manage.py createsuperuser
```

### Step 7: Run Development Server

```bash
uv run python manage.py runserver
```

## 📊 API End Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/` | Health check (database & Redis status) |
| GET | `/api/tickets/` | List all tickets (paginated) |
| POST | `/api/tickets/` | Create a new ticket |
| GET | `/api/tickets/<id>/` | Retrieve a specific ticket |
| PUT | `/api/tickets/<id>/` | Fully update a ticket |
| PATCH | `/api/tickets/<id>/` | Partially update a ticket |
| DELETE | `/api/tickets/<id>/` | Delete a ticket |
| GET | `/admin/` | Django admin interface |

## 🔧 Ticket Model Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Auto-incrementing primary key |
| `title` | String (200) | Brief summary of the issue |
| `description` | Text | Detailed description |
| `status` | Choice | `open`, `in_progress`, `resolved`, `closed` |
| `priority` | Choice | `low`, `medium`, `high`, `critical` |
| `requester_name` | String (100) | Name of the person who created the ticket |
| `requester_email` | Email | Email address of the requester |
| `created_at` | DateTime | When the ticket was created (auto) |
| `updated_at` | DateTime | When the ticket was last updated (auto) |

## 🐳 Docker Services

| Service | Container Name | Port | Description |
|---------|---------------|------|-------------|
| `web` | `ticket_manager_web` | 8000 | Django API with Gunicorn |
| `db` | `ticket_manager_db` | 5432 | PostgreSQL database |
| `redis` | `ticket_manager_redis` | 6379 | Redis cache |

## 📝 Useful Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f web

# Run Django management commands
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py showmigrations

# Rebuild after code changes
docker-compose up --build

# Remove volumes (WARNING: deletes database)
docker-compose down -v

# Check container status
docker-compose ps
```

## 🔐 Security Notes for Production

1. **Change the SECRET_KEY** - Never use the default in production
2. **Set DEBUG=False** in `.env`
3. **Use strong database passwords**
4. **Configure ALLOWED_HOSTS** with your domain
5. **Use HTTPS** in production
6. **Set up proper CORS** if needed

## 🎯 How Redis Caching Works

This project uses Redis to cache the ticket list endpoint for better performance:

1. **First Request**: Django queries PostgreSQL and returns the data
2. **Cache Storage**: The response is stored in Redis for 5 minutes
3. **Subsequent Requests**: Data is served from Redis cache (faster!)
4. **Cache Invalidation**: Cache is cleared when tickets are created, updated, or deleted

This demonstrates a realistic caching pattern you can extend to other endpoints.

## 📚 Technologies Used

- **Django 5.x** - Web framework
- **Django REST Framework** - API framework
- **PostgreSQL 15** - Production database
- **Redis 7** - Caching layer
- **Gunicorn** - Production WSGI server
- **Docker & Docker Compose** - Containerization
- **python-decouple** - Environment variable management

## 🤝 Troubleshooting

### Port Already in Use

If port 8000, 5432, or 6379 is already in use, either:
- Stop the service using that port
- Change the port mapping in `docker-compose.yml`

### Database Connection Error

Make sure PostgreSQL container is healthy:
```bash
docker-compose ps
```

### Redis Connection Error

Verify Redis is running:
```bash
docker-compose exec redis redis-cli ping
# Should return: PONG
```

### Rebuild Issues

Clear Docker cache and rebuild:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📖 License

This project is open source and available for educational purposes.
