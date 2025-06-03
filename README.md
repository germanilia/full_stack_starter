# My Boilerplate App

A full-stack application with a FastAPI backend and React frontend, designed for handling apartment management and customer service through a chatbot interface.

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework for building APIs
- **PostgreSQL**: Persistent data storage with Alembic migrations
- **AWS Cognito**: Authentication and user management
- **AWS Secrets Manager**: Secure secrets management for production
- **LocalStack**: Local AWS services simulation for development

### Frontend
- **React**: Modern UI library with TypeScript
- **Vite**: Fast build tool and development server
- **Shadcn/UI**: Modern, accessible UI components
- **TailwindCSS**: Utility-first CSS framework
- **React Router**: Client-side routing

### DevOps & Tools
- **Docker**: Containerized development and deployment
- **Just**: Command runner for development tasks
- **Alembic**: Database migration management
- **VSCode**: Integrated development environment with devcontainer support

## Project Structure

```
.
├── backend/                # FastAPI application
│   ├── app/                # Main application code
│   │   ├── core/           # Configuration and settings
│   │   ├── crud/           # Database operations
│   │   ├── db/             # Database connections and setup
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routers/        # API endpoints
│   │   └── dependencies.py # Authentication dependencies
│   ├── alembic/            # Database migrations
│   ├── secrets.example.yaml # Template for secrets configuration
│   └── Dockerfile          # Backend container setup
├── client/                 # React frontend
│   ├── public/             # Static assets
│   ├── src/                # React application code
│   │   ├── components/     # UI components (including shadcn/ui)
│   │   ├── contexts/       # React contexts (auth, etc.)
│   │   ├── lib/            # Utility functions and services
│   │   └── pages/          # Page components
│   ├── .env.development.example # Frontend environment template
│   ├── .env.production.example  # Production environment template
│   └── Dockerfile          # Frontend container setup
├── docker-compose.yml      # Multi-container setup
├── justfile               # Development commands
└── .devcontainer/         # VSCode devcontainer configuration
```

## Features

- **Authentication System**: Complete user authentication with AWS Cognito
  - Email-based usernames with automatic transformation
  - Role-based access control (Admin/User roles)
  - JWT token management with automatic refresh
  - LocalStack integration for development
- **Configuration Management**: Flexible configuration system
  - Environment-specific settings
  - AWS Secrets Manager integration for production
  - Local secrets file fallback
- **Database Management**: PostgreSQL with Alembic migrations
- **Modern Frontend**: React with TypeScript, Vite, and Shadcn/UI
- **Containerized Development**: Docker setup for consistent environments
- **Development Tools**: Just commands, VSCode integration, devcontainer support



## Prerequisites

- **Docker and Docker Compose**: For containerized development
- **Node.js 18+**: For frontend development
- **Python 3.9+**: For backend development
- **Just**: Command runner (install with `cargo install just` or package manager)
- **AWS CLI**: For production deployment (optional)

## Quick Start

### 1. Environment Setup

Copy the configuration templates and update them with your settings:

```bash
# Backend secrets (contains sensitive information)
cp backend/secrets.example.yaml backend/secrets.yaml

# Frontend configuration (contains non-sensitive information)
cp client/.env.development.example client/.env.development
cp client/.env.production.example client/.env.production
```

**Note**: Backend environment files (`.env.development`, `.env.production`, `.env.testing`) are included in source control and don't need to be copied.

### 2. Install Dependencies

```bash
# Install backend dependencies
just install

# Install frontend dependencies
cd client && npm install
```

### 3. Set Up LocalStack (Development)

Start LocalStack and create Cognito resources:

```bash
# Start LocalStack
docker-compose up localstack -d

# Create Cognito User Pool and Client
just create_cognito
```

### 4. Database Setup

```bash
# Generate and apply database migrations
just generate_migration "Initial setup"
just migrate
```

### 5. Start Development Servers

```bash
# Start both backend and frontend
just run

# Or start individually:
just run-backend  # Backend only
just run-client   # Frontend only
```

The application will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Configuration System

The application uses a flexible configuration system that loads settings from multiple sources with the following priority:

1. **Environment variables** (highest priority)
2. **AWS Secrets Manager** (if configured)
3. **Local secrets.yaml file** (fallback)
4. **Default values** (lowest priority)

### Backend Configuration

#### Environment Files (Non-sensitive)
- `.env.development`: Development environment settings
- `.env.production`: Production environment settings
- `.env.testing`: Testing environment settings

Common environment variables:
- `APP_ENV`: Environment (development, production, testing)
- `DEBUG`: Enable debug mode
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)
- `CORS_ORIGINS`: Comma-separated allowed CORS origins
- `USE_LOCALSTACK`: Use LocalStack for AWS services (development)
- `LOCALSTACK_ENDPOINT`: LocalStack endpoint URL

#### Secrets File (Sensitive Information)
The `secrets.yaml` file contains all sensitive configuration:

```yaml
# Database credentials
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
  region: "us-east-1"
  access_key_id: "your_aws_access_key_id"
  secret_access_key: "your_aws_secret_access_key"

# Cognito configuration
cognito:
  user_pool_id: "us-east-1_myid123"
  client_id: "myclient123"
  client_secret: "your_cognito_client_secret"
  endpoint_url: "http://localhost:4566"  # For LocalStack only
```

### Frontend Configuration

The frontend uses environment-specific files:
- `.env.development`: Development settings
- `.env.production`: Production settings

Key variables:
- `VITE_API_URL`: Backend API URL (e.g., http://localhost:8000)

### AWS Secrets Manager Integration (Production)

For production environments, secrets can be loaded from AWS Secrets Manager instead of the local `secrets.yaml` file.

#### Setup AWS Secrets Manager

1. **Create a secret in AWS Secrets Manager** with YAML content:
   ```yaml
   database:
     username: "postgres"
     password: "your_database_password"
     host: "your-rds-endpoint.amazonaws.com"
     port: 5432
     name: "mydatabase"

   security:
     secret_key: "your_secret_key"
     algorithm: "HS256"
     access_token_expire_minutes: 30

   aws:
     access_key_id: "your_aws_access_key_id"
     secret_access_key: "your_aws_secret_access_key"

   cognito:
     user_pool_id: "us-east-1_XXXXXXXXX"
     client_id: "your_client_id"
     client_secret: "your_client_secret"
   ```

2. **Configure environment variables** in `.env.production`:
   ```bash
   AWS_SECRETS_MANAGER_SECRET_NAME=my-app-production-secrets
   AWS_DEFAULT_REGION=us-east-1
   ```

3. **Ensure AWS credentials** are available through IAM roles, environment variables, or AWS credentials file.

**Fallback**: If AWS Secrets Manager is unavailable, the system falls back to the local `secrets.yaml` file.

## Authentication System

The application includes a complete authentication system using AWS Cognito as the primary authentication mechanism, with a development-only fallback for testing:

### Features
- **Primary Authentication**: AWS Cognito for production and development
- **Development Fallback**: Local JWT tokens for API testing (dev mode only)
- **Email-based usernames** with automatic transformation for Cognito compatibility
- **Role-based access control** (Admin/User roles)
- **JWT token management** with automatic refresh
- **LocalStack integration** for development
- **Protected routes** in both frontend and backend
- **Production Security**: Local tokens disabled in production mode

### Email-to-Username Transformation

Since Cognito has issues with @ symbols in usernames, the system automatically transforms emails:
- **Storage**: `user@domain.com` → `user_domain.com` (in Cognito)
- **Display**: `user_domain.com` → `user@domain.com` (to users)

### User Roles
- **Admin**: First user to register automatically becomes admin
- **User**: All subsequent users get user role by default

### Dual Authentication System

The system supports two authentication modes:

#### 1. Primary: AWS Cognito Authentication
- **Production**: Only Cognito tokens are accepted
- **Development**: Cognito tokens are tried first
- **Features**: Full user management, email verification, password reset
- **Token Type**: RS256 signed JWT tokens from AWS Cognito

#### 2. Fallback: Local Development Tokens (Dev Mode Only)
- **Purpose**: API testing and development without Cognito setup
- **Availability**: Only when `APP_ENV=development`
- **Security**: Automatically disabled in production
- **Token Type**: HS256 signed JWT tokens using local secret key

### Authentication Flow

#### Cognito Flow (Primary)
1. **Registration**: User registers with email and password
2. **Confirmation**: User confirms email with verification code
3. **Login**: User signs in with email and password
4. **Token Management**: JWT tokens are automatically refreshed
5. **Role Assignment**: First user becomes admin, others become users

#### Development Testing Flow (Fallback)
1. **Create Test User**: Use dev endpoint to create test user in database
2. **Generate Token**: Use dev endpoint to create local JWT token
3. **API Testing**: Use token to test protected endpoints
4. **No Cognito Required**: Skip Cognito setup for quick API testing

### API Endpoints

#### Authentication Endpoints
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/confirm-signup` - Confirm registration with verification code
- `POST /api/v1/auth/signin` - Sign in user
- `POST /api/v1/auth/refresh-token` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info
- `POST /api/v1/auth/signout` - Sign out user

#### Development Endpoints (Dev Mode Only)
- `POST /api/v1/dev/create-token` - Create local JWT token for testing
- `GET /api/v1/dev/users` - List users for token creation
- `POST /api/v1/dev/create-test-user` - Create test user in database

#### Example API Usage

**Registration:**
```json
POST /api/v1/auth/signup
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Login:**
```json
POST /api/v1/auth/signin
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Development Token Creation (Dev Mode Only):**
```json
POST /api/v1/dev/create-test-user
{}

POST /api/v1/dev/create-token
{
  "username": "testuser",
  "email": "test@example.com",
  "expires_in": 3600
}
```

**Using Development Token:**
```bash
# Get the token from the response above
curl -H "Authorization: Bearer YOUR_DEV_TOKEN" \
     http://localhost:9000/api/v1/auth/me
```

**Protected Endpoint Usage:**
```python
from app.dependencies import get_current_active_user, get_current_admin_user

# Require any authenticated user
@app.get("/protected")
async def protected_endpoint(current_user: User = Depends(get_current_active_user)):
    return {"message": "Hello authenticated user"}

# Require admin user
@app.get("/admin-only")
async def admin_endpoint(current_user: User = Depends(get_current_admin_user)):
    return {"message": "Hello admin"}
```

### Security Configuration

#### Development Mode (`APP_ENV=development`)
- **Cognito tokens**: Validated first (preferred)
- **Local tokens**: Accepted as fallback for testing
- **Secret key**: Used from `secrets.yaml` → `security.secret_key`
- **Dev endpoints**: Available at `/api/v1/dev/*`

#### Production Mode (`APP_ENV=production`)
- **Cognito tokens**: Only authentication method
- **Local tokens**: Completely disabled
- **Secret key**: Should be stored in AWS Secrets Manager
- **Dev endpoints**: Return 404 (not available)

#### Token Validation Priority
1. **Try Cognito validation** (RS256, JWKS verification)
2. **If dev mode and Cognito fails**: Try local token validation (HS256)
3. **If production and Cognito fails**: Reject token

#### Required Configuration
```yaml
# secrets.yaml (development)
security:
  secret_key: "dev_secret_key_for_testing_only_not_for_production"
  algorithm: "HS256"
  access_token_expire_minutes: 30
```

## Development Commands

### Using Just (Recommended)

```bash
# Install dependencies
just install

# Development servers
just run              # Start both backend and frontend
just run-backend      # Backend only
just run-client       # Frontend only

# Database operations
just generate_migration "migration message"
just migrate          # Apply migrations

# LocalStack setup
just create_cognito   # Create Cognito resources
just setup_localstack # Setup all LocalStack services

# Testing
just test             # Run tests
```

### Manual Commands

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Frontend
```bash
cd client
npm install
npm run dev
```

### Docker Development

```bash
# Start all services
docker-compose up

# Start specific services
docker-compose up backend frontend postgres
docker-compose up localstack  # For AWS services simulation
```

## Frontend Development

### Project Structure
- `src/components/`: React components including Shadcn/UI components
- `src/contexts/`: React contexts for state management (AuthContext)
- `src/lib/`: Utility functions and services (API client, config)
- `src/pages/`: Page components for routing

### Key Components
- **AuthContext**: Manages authentication state and token handling
- **ProtectedRoute**: Wrapper for route protection
- **LoginForm/RegisterForm**: Authentication forms
- **API Client**: Centralized API communication

### Adding Environment Variables
1. Add variable to appropriate `.env` files
2. Add type to `src/vite-env.d.ts`
3. Add to `AppConfig` interface in `src/lib/config.ts`
4. Add getter function in `config.ts`

## Testing

### Backend Testing
```bash
cd backend
pytest                    # Run all tests
pytest tests/test_auth.py # Run specific test file
pytest -v                # Verbose output
```

### Frontend Testing
```bash
cd client
npm test                 # Run tests
npm run test:coverage    # Run with coverage
```

### Integration Testing

#### Cognito Authentication Testing
Test the complete authentication flow:
1. Register new user → Confirm email → Login
2. Test role assignment (first user = admin)
3. Test protected routes and API endpoints
4. Test token refresh functionality

#### Development Token Testing
Quick API testing without Cognito setup:
```bash
# 1. Create test user
curl -X POST http://localhost:9000/api/v1/dev/create-test-user

# 2. Generate development token
curl -X POST http://localhost:9000/api/v1/dev/create-token \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "expires_in": 3600}'

# 3. Test protected endpoint
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     http://localhost:9000/api/v1/auth/me

# 4. Test admin endpoint (if testuser has admin role)
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     http://localhost:9000/api/v1/admin-endpoint
```

#### Authentication Priority Testing
1. **With valid Cognito token**: Should use Cognito validation
2. **With invalid Cognito + valid local token (dev)**: Should fallback to local
3. **With invalid tokens in production**: Should reject all tokens
4. **Dev endpoints in production**: Should return 404

## Troubleshooting

### Common Issues

**Authentication Errors:**
- "Authentication required": Token expired → Sign out and sign in again
- "User not found": User exists in Cognito but not in database → Sign in again
- "Invalid token": Check JWT token validity and expiration
- "Token validation failed": In dev mode, check both Cognito and local token formats
- "Development endpoints not available": Ensure `APP_ENV=development`
- "Local tokens not allowed": Trying to use dev tokens in production mode

**LocalStack Issues:**
- "Failed to fetch JWKS": Ensure LocalStack is running and Cognito is set up
- Check LocalStack logs: `docker logs localstack`
- Confirmation codes appear in LocalStack logs during development

**CORS Errors:**
- Update `CORS_ORIGINS` in backend environment files
- Ensure frontend URL is included in allowed origins

**Database Issues:**
- Connection failed: Check database credentials in `secrets.yaml`
- Migration errors: Ensure database exists and is accessible

### Debug Mode

Enable debug logging:
```bash
# Backend
LOG_LEVEL=DEBUG

# Frontend (development builds include console.log statements)
npm run dev
```

## Production Deployment

### Backend Deployment
1. **Set up AWS Secrets Manager** with production secrets
2. **Configure environment variables**:
   ```bash
   APP_ENV=production
   USE_LOCALSTACK=False
   AWS_SECRETS_MANAGER_SECRET_NAME=my-app-production-secrets
   ```
3. **Set up real AWS Cognito** User Pool and Client
4. **Configure database** (RDS recommended)
5. **Set up CORS** for production domain

### Frontend Deployment
1. **Update environment variables** in `.env.production`
2. **Build for production**: `npm run build`
3. **Deploy static files** to CDN/hosting service
4. **Configure routing** for SPA (single-page application)

### Security Considerations
- Use HTTPS in production
- Store secrets in AWS Secrets Manager
- Configure proper CORS origins
- Set appropriate token expiration times
- Monitor authentication logs
- Use IAM roles for AWS service access

## VSCode Integration

### Features
- **Debugging**: Backend and frontend debugging configurations
- **Development Container**: Pre-configured development environment
- **Code Formatting**: ESLint, Prettier, Black configurations
- **Extensions**: Recommended extensions for Python, TypeScript, React

### Development Container Setup
1. Install [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
2. Open project in VSCode
3. Click green button in lower left → "Reopen in Container"
4. Container includes all necessary tools pre-installed

## Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** following the coding standards
4. **Write tests** for new functionality
5. **Run tests** to ensure everything works
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open Pull Request**

### Coding Standards
- **Backend**: Follow PEP 8, use type hints, write docstrings
- **Frontend**: Use TypeScript, follow ESLint rules, use Prettier
- **Testing**: Write tests for new features and bug fixes
- **Documentation**: Update README and inline documentation