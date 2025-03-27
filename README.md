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

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your configuration

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