# Backend Application

This is the backend for the My Boilerplate App, built with FastAPI.

## Configuration System

The application uses a flexible configuration system that loads settings from multiple sources:

1. Environment-specific `.env` files (for non-sensitive configuration)
2. Secrets YAML file (for sensitive information)
3. Default values

### Environment Configuration

The application supports different environments through environment-specific configuration files:

- `.env.development`: Development environment settings
- `.env.production`: Production environment settings
- `.env.testing`: Testing environment settings

The environment is determined by the `APP_ENV` environment variable, which defaults to `development`.

Common environment variables include:

- `APP_ENV`: The environment (development, production, testing)
- `DEBUG`: Whether to enable debug mode
- `PORT`: The port to run the server on
- `HOST`: The host to bind the server to
- `CORS_ORIGINS`: Comma-separated list of allowed CORS origins

**Important**: No secrets or sensitive information should be stored in these files.

### Secrets File

Sensitive information is stored in a `secrets.yaml` file, which should never be committed to version control. The file structure is:

```yaml
# Database credentials and connection information
database:
  username: "postgres"
  password: "your_password"
  host: "localhost"
  port: 5432
  name: "mydatabase"
  url: "postgresql://postgres:your_password@localhost:5432/mydatabase"

# Security settings
security:
  secret_key: "your_secret_key"
  algorithm: "HS256"
  access_token_expire_minutes: 30

# AWS credentials
aws:
  access_key_id: "your_aws_access_key_id"
  secret_access_key: "your_aws_secret_access_key"
```

A template file `secrets.example.yaml` is provided with placeholders.

### Configuration System

The configuration system in `app/core/config_service.py` provides two ways to access configuration:

1. **ConfigService**: Low-level access to configuration values
2. **Settings**: Pydantic model with typed configuration values

#### ConfigService

The `ConfigService` class handles loading and accessing configuration from all sources. It provides methods to:

- Get configuration values with fallbacks
- Get environment-specific values
- Construct database URLs
- Check the current environment

#### Settings

The `Settings` class is a Pydantic model that provides typed access to configuration values. It's the recommended way to access configuration in most cases.

### Usage

To access configuration in your code:

```python
# Recommended: Use the Settings model for typed access
from app.core.config_service import settings

# Access typed configuration values
api_prefix = settings.API_V1_STR
debug_mode = settings.DEBUG
database_url = settings.DATABASE_URL

# For advanced cases: Use the ConfigService directly
from app.core.config_service import config_service

# Get a simple value
debug_mode = config_service.get("debug", False)

# Get a nested value from secrets
db_password = config_service.get("database.password")

# Use helper methods
db_url = config_service.get_database_url()
secret_key = config_service.get_secret_key()

# Check environment
if config_service.is_development():
    # Development-specific code
```

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# Run with custom port
uvicorn app.main:app --reload --port 8000
```
