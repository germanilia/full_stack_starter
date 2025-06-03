# My Boilerplate App

A full-stack application with a FastAPI backend and React frontend, designed for handling apartment management and customer service through a chatbot interface.

## Project Structure

```
.
├── backend/                # FastAPI application
│   ├── app/                # Main application code
│   │   ├── core/           # Configuration and settings
│   │   ├── crud/           # Database operations
│   │   ├── db/             # Database connections
│   │   ├── models/         # SQL Alchemy models
│   │   └── routers/        # API endpoints
│   ├── alembic/            # Database migrations
│   └── Dockerfile          # Backend container setup
├── client/                 # React frontend
│   ├── public/             # Static assets
│   ├── src/                # React application code
│   │   └── components/     # UI components (including shadcn/ui)
│   └── Dockerfile          # Frontend container setup
└── docker-compose.yml      # Multi-container setup
```

## Features

- **FastAPI Backend**: Modern Python web framework for building APIs
- **React Frontend**: UI built with React
- **PostgreSQL Database**: Persistent data storage
- **Containerized**: Docker setup for consistent development and deployment
- **Shadcn/UI Components**: Modern UI components for the frontend
- **TailwindCSS**: Utility-first CSS framework

## API Objects

### Request Object

```json
{
  "session_id": "12345abcde",
  "user_id": "tenant123",
  "booking_number": "BK78901",
  "conversation_history": [
    {
      "role": "user",
      "message": "I'd like to extend my stay for 3 more days",
      "timestamp": "2023-11-15T14:30:00Z"
    },
    {
      "role": "assistant",
      "message": "I'd be happy to help you with that. Let me check the availability.",
      "timestamp": "2023-11-15T14:30:15Z"
    }
  ],
  "apartment_information": {
    "apartment_id": "APT456",
    "location": {
      "address": "123 Beach Avenue",
      "city": "Tel Aviv",
      "country": "Israel"
    },
    "wifi_details": {
      "network_name": "Sweetinn_Guest",
      "password": "welcomeguest2023"
    },
    "available_services": [
      {
        "service_type": "car_service",
        "description": "Car rental with delivery to apartment",
        "contact": "+972123456789"
      },
      {
        "service_type": "food_delivery",
        "description": "Local restaurant partnerships with discount"
      }
    ]
  }
}
```

### Response Object

```json
{
  "session_id": "12345abcde",
  "response_type": "answer",
  "message": "I've checked and your apartment is available for a 3-day extension. The total cost for the additional days would be $450. Would you like me to book this extension for you?",
  "confidence_score": 0.92,
  "intent_detected": "extend_stay"
}
```

### Information Request Object

```json
{
  "session_id": "12345abcde",
  "response_type": "request_info",
  "required_information": {
    "type": "availability_check",
    "parameters": {
      "apartment_id": "APT456",
      "check_in_date": "2023-11-20",
      "check_out_date": "2023-11-23"
    }
  },
  "user_message": "I need to check if we can extend your stay. What dates were you considering?"
}
```

## System Flow

1. **Request Flow**:
   - The backend sends an API request with user query and context
   - Requests include booking information, conversation history, and apartment details

2. **Processing Flow**:
   - The Bot Service processes requests through:
     - Intent Recognition: Determines what the user wants
     - Reasoning Engine: Analyzes the request against available knowledge
     - Response Generation: Creates appropriate responses

3. **Storage Components**:
   - AWS OpenSearch: Stores vector embeddings for semantic searching
   - AWS S3: Stores knowledge base documents, FAQs, and policies

4. **Response Flow**:
   - The bot returns either:
     - A direct answer to the user's query
     - A request for additional information needed to fulfill the request

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js (for local development)
- Python 3.9+ (for local development)

### Environment Setup

1. Copy the secrets file and frontend environment files:
   ```bash
   # Backend secrets (contains sensitive information)
   cp backend/secrets.example.yaml backend/secrets.yaml

   # Frontend configuration (contains non-sensitive information)
   cp client/.env.development.example client/.env.development
   cp client/.env.production.example client/.env.production
   ```

   Note: Backend environment files (.env.development, .env.production, .env.testing) are included in source control and don't need to be copied.

2. Edit the environment files and secrets file with your configuration

#### Backend Configuration
The backend uses two types of configuration files:

1. **Environment-specific files** (non-sensitive configuration):
   - `.env.development`: Development environment settings
   - `.env.production`: Production environment settings
   - `.env.testing`: Testing environment settings

2. **Secrets file** (sensitive information):
   - `secrets.yaml`: Contains all sensitive information like database credentials, AWS keys, etc.
   - Structure includes database credentials and AWS access keys
   - **For production**: Use AWS Secrets Manager instead of local secrets file

#### Frontend Configuration
The frontend uses environment-specific files:
- `.env.development`: Used during development (`npm run dev`)
- `.env.production`: Used for production builds (`npm run build`)

Key frontend environment variables:
- `VITE_API_URL`: The URL of the backend API

**Important**: All sensitive information should be stored in the backend's `secrets.yaml` file, not in any `.env` files.

### AWS Secrets Manager Integration (Production)

For production environments, the application supports loading secrets from AWS Secrets Manager instead of the local `secrets.yaml` file. This provides better security and centralized secret management.

#### Setup AWS Secrets Manager

1. **Create a secret in AWS Secrets Manager** with YAML content matching your `secrets.yaml`:
   ```yaml
   database:
     username: "postgres"
     password: "your_database_password"
     host: "your-rds-endpoint.amazonaws.com"
     port: 5432
     name: "mydatabase"
     url: "postgresql://postgres:password@your-rds-endpoint.amazonaws.com:5432/mydatabase"

   security:
     secret_key: "your_secret_key"
     algorithm: "HS256"
     access_token_expire_minutes: 30

   aws:
     access_key_id: "your_aws_access_key_id"
     secret_access_key: "your_aws_secret_access_key"
   ```

2. **Configure environment variables** in your `.env.production`:
   ```bash
   AWS_SECRETS_MANAGER_SECRET_NAME=my-app-production-secrets
   AWS_DEFAULT_REGION=us-east-1
   ```

3. **Ensure AWS credentials** are available through:
   - IAM roles (recommended for EC2/ECS)
   - Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
   - AWS credentials file
   - Instance metadata service

#### Fallback Behavior

The configuration system follows this priority order:
1. **Environment variables** (highest priority)
2. **AWS Secrets Manager** (if configured)
3. **Local secrets.yaml file** (fallback)
4. **Default values** (lowest priority)

If a secret is missing from AWS Secrets Manager, the system will automatically fall back to the local `secrets.yaml` file for that specific secret.

### Running with Docker

```bash
docker-compose up
```

### Development Commands

Using the `just` command runner:

```bash
# Install backend dependencies
just install

# Run the backend server
just run-backend

# Run the frontend server
just run-client

# Run both servers
just run

# Generate a new database migration
just migrate-generate "migration message"

# Run database migrations
just migrate-run
```

## VSCode Integration

This project includes VSCode configurations for:
- Debugging the backend and frontend
- Running both servers simultaneously
- Code formatting and linting

## Development Container

A development container is provided with all necessary tools pre-installed. To use it:

1. Install the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
2. Open the project in VSCode
3. Click on the green button in the lower left corner and select "Reopen in Container"