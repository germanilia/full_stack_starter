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
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container setup
├── client/                 # React frontend
│   ├── public/             # Static assets
│   ├── src/                # React application code
│   │   ├── components/     # UI components (including shadcn/ui)
│   │   │   ├── ui/         # Shadcn/UI base components
│   │   │   └── forms/      # Form components (login, signup, etc.)
│   │   ├── contexts/       # React contexts (auth, etc.)
│   │   ├── hooks/          # Custom React hooks
│   │   ├── lib/            # Utility functions and services
│   │   ├── pages/          # Page components
│   │   └── types/          # TypeScript type definitions
│   ├── .env.development.example # Frontend environment template
│   ├── .env.production.example  # Production environment template
│   ├── package.json        # Frontend dependencies
│   ├── tailwind.config.js  # TailwindCSS configuration
│   ├── vite.config.ts      # Vite configuration
│   └── Dockerfile          # Frontend container setup
├── docker-compose.yml      # Multi-container setup
├── justfile               # Development commands
└── .devcontainer/         # VSCode devcontainer configuration
```

## Features

- **Authentication System**: Complete user authentication with AWS Cognito
  - Email-based usernames (no transformation needed)
  - Role-based access control (Admin/User roles)
  - JWT token management with automatic refresh
  - Auto-confirmation in development mode
  - User-friendly error messages
  - Environment-based configuration
- **Dark Mode Support**: Complete dark/light theme system with proper styling
- **Responsive Design**: Mobile-first responsive UI components
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

### 3. Set Up AWS Cognito

Create Cognito User Pool and Client on real AWS:

```bash
# For development environment
just create_cognito_dev

# For production environment
just create_cognito_prod

# Or use the generic command (uses development by default)
just create_cognito
```

The command will automatically add the Cognito configuration to your environment file:

```bash
# The command automatically adds these lines to backend/.env.development:
# COGNITO_USER_POOL_ID=us-west-2_ABC123DEF
# COGNITO_CLIENT_ID=1a2b3c4d5e6f7g8h9i0j

# A backup is created before modification (.env.development.backup)
```

**Note**: This creates real AWS Cognito resources with minimal configuration for easy development. The User Pool will have:
- Simple password requirements (8 characters minimum)
- No email verification required in development
- Auto-confirmation enabled for development
- Email as username (no transformation needed)

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

## Frontend Development

### Styling and Theming

The application uses TailwindCSS with Shadcn/UI components and supports both light and dark themes:

#### Dark Mode Implementation
- **Theme Toggle**: Available in the navigation/header
- **Automatic Detection**: Respects system preference by default
- **Persistent Storage**: Theme preference saved to localStorage
- **Component Styling**: All components properly styled for both themes

#### Common Dark Mode Classes
```css
/* Background colors */
bg-background          /* Main background (white/dark) */
bg-card               /* Card background */
bg-popover            /* Popover/modal background */
bg-muted              /* Muted background */

/* Text colors */
text-foreground       /* Main text color */
text-muted-foreground /* Muted text color */
text-card-foreground  /* Card text color */

/* Border colors */
border-border         /* Standard border */
border-input          /* Input border */
```

#### Form Components
All form components (login, signup, etc.) are styled with:
- Proper dark mode support using CSS variables
- Consistent spacing and typography
- Accessible focus states
- Responsive design

### Project Structure (Frontend)

```
client/src/
├── components/
│   ├── ui/              # Shadcn/UI base components
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── card.tsx
│   │   └── ...
│   ├── forms/           # Form components
│   │   ├── LoginForm.tsx
│   │   ├── SignupForm.tsx
│   │   └── ...
│   ├── layout/          # Layout components
│   │   ├── Header.tsx
│   │   ├── Sidebar.tsx
│   │   └── ThemeToggle.tsx
│   └── ...
├── contexts/
│   ├── AuthContext.tsx  # Authentication state
│   └── ThemeContext.tsx # Theme state
├── hooks/
│   ├── useAuth.ts
│   ├── useTheme.ts
│   └── ...
├── lib/
│   ├── api.ts          # API client
│   ├── config.ts       # Configuration
│   ├── utils.ts        # Utility functions
│   └── validations.ts  # Form validations
├── pages/
│   ├── LoginPage.tsx
│   ├── SignupPage.tsx
│   ├── Dashboard.tsx
│   └── ...
└── types/
    ├── auth.ts
    ├── api.ts
    └── ...
```

### Key Components

#### Authentication Components
- **AuthContext**: Manages authentication state and token handling
- **ProtectedRoute**: Wrapper for route protection
- **LoginForm/SignupForm**: Authentication forms with proper dark mode styling
- **API Client**: Centralized API communication

#### Theme Components
- **ThemeContext**: Manages theme state (light/dark)
- **ThemeToggle**: Toggle component for switching themes
- **Theme Provider**: Applies theme classes to the application

### Adding New Components

When creating new components, ensure they support dark mode:

```tsx
// Example component with proper dark mode support
const MyComponent = () => {
  return (
    <div className="bg-background text-foreground border border-border">
      <h1 className="text-foreground">Title</h1>
      <p className="text-muted-foreground">Description</p>
    </div>
  );
};
```

### Environment Variables
1. Add variable to appropriate `.env` files
2. Add type to `src/vite-env.d.ts`
3. Add to `AppConfig` interface in `src/lib/config.ts`
4. Add getter function in `config.ts`

## Backend Development

### Project Structure (Backend)

```
backend/
├── app/
│   ├── core/
│   │   ├── config.py      # Configuration management
│   │   ├── security.py    # Security utilities
│   │   └── database.py    # Database connection
│   ├── crud/
│   │   ├── base.py        # Base CRUD operations
│   │   ├── user.py        # User CRUD operations
│   │   └── ...
│   ├── db/
│   │   ├── base.py        # SQLAlchemy base
│   │   ├── session.py     # Database session
│   │   └── init_db.py     # Database initialization
│   ├── models/
│   │   ├── base.py        # Base model
│   │   ├── user.py        # User model
│   │   └── ...
│   ├── routers/
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── users.py       # User management
│   │   ├── admin.py       # Admin endpoints
│   │   └── ...
│   ├── schemas/
│   │   ├── user.py        # User Pydantic models
│   │   ├── auth.py        # Auth Pydantic models
│   │   └── ...
│   ├── services/
│   │   ├── auth_service.py     # Authentication business logic
│   │   ├── cognito_service.py  # AWS Cognito integration
│   │   └── ...
│   ├── dependencies.py    # FastAPI dependencies
│   └── main.py           # FastAPI application
├── alembic/              # Database migrations
├── tests/                # Test files
├── secrets.example.yaml  # Secrets template
├── requirements.txt      # Python dependencies
└── Dockerfile           # Container configuration
```

### API Development

#### Creating New Endpoints
1. **Define Pydantic schemas** in `schemas/`
2. **Create CRUD operations** in `crud/`
3. **Add router endpoints** in `routers/`
4. **Include router** in `main.py`

#### Example API Endpoint
```python
# schemas/example.py
from pydantic import BaseModel

class ExampleCreate(BaseModel):
    name: str
    description: str

class ExampleResponse(BaseModel):
    id: int
    name: str
    description: str

# routers/example.py
from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/api/v1/examples", tags=["examples"])

@router.post("/", response_model=ExampleResponse)
async def create_example(
    example: ExampleCreate,
    current_user: User = Depends(get_current_active_user)
):
    # Implementation here
    pass
```

### Database Management

#### Creating Migrations
```bash
# Generate new migration
just generate_migration "Add new table"

# Apply migrations
just migrate

# Downgrade migration
alembic downgrade -1
```

#### Model Development
```python
# models/example.py
from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base

class Example(Base):
    __tablename__ = "examples"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
```

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
- `COGNITO_REGION`: AWS region for Cognito (default: us-east-1)
- `COGNITO_POOL_NAME`: Cognito User Pool name
- `COGNITO_CLIENT_NAME`: Cognito User Pool Client name
- `COGNITO_USER_POOL_ID`: Cognito User Pool ID (from create_cognito output)
- `COGNITO_CLIENT_ID`: Cognito Client ID (from create_cognito output)

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

# Note: Cognito configuration is now stored in environment files (.env.development, .env.production)
# not in secrets.yaml. See environment variables section above.
```

### Frontend Configuration

The frontend uses environment-specific files:
- `.env.development`: Development settings
- `.env.production`: Production settings

Key variables:
- `VITE_API_URL`: Backend API URL (e.g., http://localhost:8000)
- `VITE_APP_TITLE`: Application title
- `VITE_DEFAULT_THEME`: Default theme (light/dark)

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
     user_pool_id: "us-east-1_XXXXXXXXX"  # From create_cognito output
     client_id: "your_client_id"          # From create_cognito output
     region: "us-east-1"                  # Should match COGNITO_REGION
   ```

2. **Configure environment variables** in `.env.production`:
   ```bash
   AWS_SECRETS_MANAGER_SECRET_NAME=my-app-production-secrets
   AWS_DEFAULT_REGION=us-east-1
   ```

3. **Ensure AWS credentials** are available through IAM roles, environment variables, or AWS credentials file.

**Fallback**: If AWS Secrets Manager is unavailable, the system falls back to the local `secrets.yaml` file.

## AWS Cognito Setup

The application uses AWS Cognito for authentication. Cognito resources are created using the justfile commands and configured via environment variables.

### Cognito Configuration

Cognito settings are managed through environment variables in `.env.development` and `.env.production`:

```bash
# Development environment (.env.development)
COGNITO_REGION=us-west-2
COGNITO_POOL_NAME=MyAppUserPool-Dev
COGNITO_CLIENT_NAME=MyAppClient-Dev
# These are added after running 'just create_cognito_dev':
COGNITO_USER_POOL_ID=us-west-2_ABC123DEF
COGNITO_CLIENT_ID=1a2b3c4d5e6f7g8h9i0j

# Production environment (.env.production)
COGNITO_REGION=us-west-2
COGNITO_POOL_NAME=MyAppUserPool-Prod
COGNITO_CLIENT_NAME=MyAppClient-Prod
# These are added after running 'just create_cognito_prod':
COGNITO_USER_POOL_ID=us-west-2_XYZ789ABC
COGNITO_CLIENT_ID=9z8y7x6w5v4u3t2s1r0q
```

### Creating Cognito Resources

Use the justfile commands to create Cognito User Pools and Clients:

```bash
# Create for development
just create_cognito_dev

# Create for production
just create_cognito_prod

# Create for current environment (based on APP_ENV)
just create_cognito
```

### After Creation

After running the create_cognito command, you'll get output like:

```
🎉 Cognito setup complete for environment: development
User Pool Name: MyAppUserPool-Dev
User Pool ID: us-west-2_ABC123DEF
Client Name: MyAppClient-Dev
Client ID: 1a2b3c4d5e6f7g8h9i0j
Region: us-west-2

📝 Updating .env.development file...
✓ Added Cognito configuration to .env.development
✓ Backup saved as .env.development.backup

🎉 Cognito setup complete! Your backend will automatically use the new configuration.
```

The command automatically adds the Cognito IDs to your environment file and creates a backup. No manual configuration needed!

### Cognito Features

The created User Pools have these characteristics:
- **Simple passwords**: 8 characters minimum, no complexity requirements
- **Email usernames**: Users sign in with their email address (no transformation needed)
- **Auto-confirmation**: Users are auto-confirmed in development mode (no email verification)
- **User-friendly errors**: Meaningful error messages instead of generic API errors
- **Multiple auth flows**: Supports password auth, SRP auth, and refresh tokens
- **Environment-based config**: Configuration stored in environment files, not secrets

### Deleting Cognito Resources

To clean up Cognito resources:

```bash
# Delete development Cognito resources
just delete_cognito_dev

# Delete production Cognito resources
just delete_cognito_prod

# Delete for current environment
just delete_cognito
```

**Note**: The delete command reads the User Pool ID and Client ID from your environment variables, deletes the AWS resources, and then automatically removes the `COGNITO_USER_POOL_ID` and `COGNITO_CLIENT_ID` lines from your `.env` file. A backup is created before modification.

## Authentication System

The application includes a complete authentication system using AWS Cognito as the primary authentication mechanism, with a development-only fallback for testing:

### Features
- **Primary Authentication**: AWS Cognito for production and development
- **Development Fallback**: Local JWT tokens for API testing (dev mode only)
- **Email-based usernames** for seamless user experience
- **Role-based access control** (Admin/User roles)
- **JWT token management** with automatic refresh
- **LocalStack integration** for development
- **Protected routes** in both frontend and backend
- **Production Security**: Local tokens disabled in production mode

### Email Username Support

The system uses email addresses directly as usernames in Cognito:
- **Direct email usage**: `user@domain.com` is used as-is in Cognito
- **Cognito configuration**: User Pool is configured with `username_attributes = ["email"]`
- **Seamless experience**: Users sign in with their email address

### User Roles and Admin System

The application implements an automatic admin assignment system:

#### Admin Role Assignment
- **First User**: The very first user to register automatically becomes an admin
- **Subsequent Users**: All users after the first become regular users by default
- **Database Check**: The system checks the user count in the database before creating each user
- **Automatic Assignment**: No manual intervention required - the first user is automatically promoted

#### Role Capabilities
- **Admin Role (`admin`)**:
  - Full access to all application features
  - Can manage other users (future feature)
  - Access to admin-only endpoints
  - Automatically assigned to the first user

- **User Role (`user`)**:
  - Standard application access
  - Cannot access admin-only features
  - Default role for all users after the first

#### Implementation Details
The admin assignment logic is implemented in multiple layers:
- **UserDAO**: Checks user count and assigns admin role if count is 0
- **UserService**: Inherits the same logic through DAO
- **Authentication Flow**: Works during both signup and signin processes
- **Database Persistence**: Role is stored in the database and persists across sessions

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

#### Testing Admin Role Assignment

You can test the admin role assignment system:

1. **Clear Database**: Ensure you start with an empty user table
2. **Register First User**: Use the signup endpoint or frontend
3. **Check Role**: The first user should have `"role": "admin"` in the response
4. **Register Second User**: Create another user
5. **Verify Role**: The second user should have `"role": "user"`

**Example API Test:**
```bash
# First user (becomes admin)
curl -X POST "http://localhost:9000/api/v1/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@example.com",
       "password": "SecurePass123!",
       "full_name": "Admin User"
     }'

# Sign in and check role
curl -X POST "http://localhost:9000/api/v1/auth/signin" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@example.com",
       "password": "SecurePass123!"
     }'
# Response will include: "user": {"role": "admin", ...}
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

# Cognito management
just create_cognito_dev   # Create Cognito resources for development
just create_cognito_prod  # Create Cognito resources for production
just delete_cognito_dev   # Delete Cognito resources for development
just delete_cognito_prod  # Delete Cognito resources for production

# LocalStack setup (if using LocalStack)
just setup_localstack # Setup all LocalStack services

# Testing
just test             # Run all tests
just test-backend     # Backend tests only
just test-frontend    # Frontend tests only

# Code quality
just lint             # Run linters
just format           # Format code
```

### Manual Commands

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Testing
pytest
pytest tests/test_auth.py
pytest -v --cov=app

# Code quality
black .
isort .
flake8 .
mypy .
```

#### Frontend
```bash
cd client
npm install
npm run dev

# Testing
npm test
npm run test:coverage
npm run test:watch

# Code quality
npm run lint
npm run lint:fix
npm run type-check
```

### Docker Development

```bash
# Start all services
docker-compose up

# Start specific services
docker-compose up backend frontend postgres
docker-compose up localstack  # For AWS services simulation

# Development with hot reload
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

## Testing

### Backend Testing

#### Running Tests
```bash
cd backend

# Install test dependencies first
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run specific test categories
pytest tests/unit/                    # Unit tests only
pytest tests/integration/             # Integration tests only

# Run specific test files
pytest tests/unit/test_user_dao.py    # User DAO tests
pytest tests/unit/test_auth_endpoints.py  # Auth endpoint tests
pytest tests/integration/test_auth_admin_flow.py  # Admin flow tests

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=app
```

#### Admin Role Tests
The application includes comprehensive tests for the admin role assignment system:

**Unit Tests** (`tests/unit/`):
- `test_user_dao.py`: Tests admin assignment in UserDAO
- `test_user_service.py`: Tests admin assignment in UserService
- `test_auth_endpoints.py`: Tests admin role in authentication endpoints

**Integration Tests** (`tests/integration/`):
- `test_auth_admin_flow.py`: End-to-end admin role assignment testing
- `test_cognito_setup.py`: Cognito integration tests

**Key Test Scenarios**:
- First user becomes admin
- Second user becomes regular user
- Admin role persists in database
- Authentication flow preserves admin role
- Signup/signin endpoints return correct roles

#### Test Structure
```
backend/tests/
├── conftest.py                      # Test configuration and fixtures
├── unit/                           # Unit tests
│   ├── test_user_dao.py           # UserDAO tests (includes admin logic)
│   ├── test_user_service.py       # UserService tests
│   └── test_auth_endpoints.py     # Authentication endpoint tests
└── integration/                    # Integration tests
    ├── test_auth_admin_flow.py    # Admin role assignment flow
    └── test_cognito_setup.py      # Cognito integration tests
```

### Frontend Testing
```bash
cd client
npm test                 # Run tests
npm run test:coverage    # Run with coverage
npm run test:watch       # Watch mode
npm run test:ui          # UI test runner
```

Test structure:
```
client/src/
├── __tests__/           # Test files
│   ├── components/
│   ├── hooks/
│   ├── pages/
│   └── utils/
├── __mocks__/           # Mock files
└── test-utils.tsx       # Testing utilities
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

### End-to-End Testing

Using Playwright for E2E tests:
```bash
# Frontend E2E tests
cd client
npm run test:e2e
npm run test:e2e:ui      # With UI
npm run test:e2e:debug   # Debug mode
```

## Troubleshooting

### Common Issues

**Authentication Errors:**
- "Authentication required": Token expired → Sign out and sign in again
- "User not found": User exists in Cognito but not in database → Sign in again
- "Invalid token": Check JWT token validity and expiration
- "Token validation failed": In dev mode, check both Cognito and local token formats
- "Development endpoints not available": Ensure `APP_ENV=development`
- "Local tokens not allowed": Trying to use dev tokens in production mode
- "Invalid email or password": Check credentials, user may not exist or be confirmed
- "User account is not confirmed": In development, users should be auto-confirmed
- "Temporary password has expired": Reset password or contact admin

**Cognito Configuration Errors:**
- "COGNITO_USER_POOL_ID not found": Check environment variables in `.env.development`
- "Cognito client initialization failed": Verify AWS credentials and region
- "User Pool not found": Run `just create_cognito_dev` to create resources
- "Multiple User Pools found": Delete duplicate pools manually in AWS Console

**Frontend/Styling Issues:**
- **Dark mode not working**: Check if ThemeProvider is properly configured
- **Components not styled**: Ensure TailwindCSS is properly imported
- **White background in dark mode**: Check component uses `bg-background` instead of `bg-white`
- **Theme not persisting**: Check localStorage permissions and ThemeContext

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

**Build Issues:**
- **Frontend build fails**: Check TypeScript errors, missing dependencies
- **Backend start fails**: Check Python dependencies, environment variables
- **Docker build fails**: Check Dockerfile syntax, build context

### Debug Mode

Enable debug logging:
```bash
# Backend
LOG_LEVEL=DEBUG

# Frontend (development builds include console.log statements)
npm run dev

# Docker with debug
docker-compose -f docker-compose.yml -f docker-compose.debug.yml up
```

### Performance Issues

**Backend Performance:**
- Enable SQL query logging: `SQLALCHEMY_ECHO=true`
- Use database connection pooling
- Implement caching for frequent queries
- Monitor with `uvicorn --log-level debug`

**Frontend Performance:**
- Use React DevTools Profiler
- Check bundle size: `npm run build -- --analyze`
- Optimize images and assets
- Implement code splitting

## Production Deployment

### Backend Deployment

#### AWS Deployment (Recommended)
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

#### Docker Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with production configuration
docker-compose -f docker-compose.prod.yml up -d
```

#### Environment Variables (Production)
```bash
# Required production environment variables
APP_ENV=production
DEBUG=False
USE_LOCALSTACK=False
CORS_ORIGINS=https://yourdomain.com
AWS_SECRETS_MANAGER_SECRET_NAME=your-secret-name
AWS_DEFAULT_REGION=us-east-1
```

### Frontend Deployment

#### Static Site Deployment
1. **Update environment variables** in `.env.production`
2. **Build for production**: `npm run build`
3. **Deploy static files** to CDN/hosting service (Vercel, Netlify, S3+CloudFront)
4. **Configure routing** for SPA (single-page application)

#### Production Environment Variables
```bash
# .env.production
VITE_API_URL=https://api.yourdomain.com
VITE_APP_TITLE=Your App Name
VITE_DEFAULT_THEME=light
```

#### Build Configuration
```bash
# Build for production
npm run build

# Preview production build locally
npm run preview

# Analyze bundle size
npm run build -- --analyze
```

### Security Considerations

#### Backend Security
- Use HTTPS in production
- Store secrets in AWS Secrets Manager
- Configure proper CORS origins
- Set appropriate token expiration times
- Monitor authentication logs
- Use IAM roles for AWS service access
- Enable request rate limiting
- Use security headers (HSTS, CSP, etc.)

#### Frontend Security
- Implement Content Security Policy (CSP)
- Use HTTPS for all resources
- Sanitize user inputs
- Avoid storing sensitive data in localStorage
- Implement proper error boundaries
- Use secure authentication flows

#### Database Security
- Use connection pooling
- Enable SSL connections
- Implement proper access controls
- Regular security updates
- Monitor for suspicious activity
- Backup and disaster recovery

### Monitoring and Logging

#### Backend Monitoring
```python
# Add to main.py for production logging
import logging
from app.core.config import settings

if settings.app_env == "production":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
```

#### Frontend Monitoring
- Implement error tracking (Sentry, LogRocket)
- Monitor performance metrics
- Track user analytics
- Set up uptime monitoring

#### Infrastructure Monitoring
- AWS CloudWatch for AWS resources
- Application performance monitoring (APM)
- Database performance monitoring
- Load balancer health checks

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

### Recommended Extensions
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.isort",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.vscode-typescript-next",
    "ms-vscode-remote.remote-containers",
    "ms-vscode.vscode-json"
  ]
}
```

### Debug Configuration
The project includes debug configurations for:
- FastAPI backend debugging
- React frontend debugging
- Full-stack debugging
- Testing debugging

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

#### Backend Standards
- **Follow PEP 8** for Python code style
- **Use type hints** for all function parameters and returns
- **Write docstrings** for all functions and classes
- **Use explicit imports** instead of wildcard imports
- **Prefer composition over inheritance**
- **Write unit tests** for new functionality

```python
# Good example
def create_user(
    db: Session, 
    user_create: UserCreate
) -> User:
    """Create a new user in the database.
    
    Args:
        db: Database session
        user_create: User creation data
        
    Returns:
        Created user instance
        
    Raises:
        ValueError: If email already exists
    """
    # Implementation here
    pass
```

#### Frontend Standards
- **Use TypeScript** for all new code
- **Follow ESLint rules** and Prettier formatting
- **Use functional components** with hooks
- **Implement proper error boundaries**
- **Write unit tests** for components and utilities

```tsx
// Good example
interface UserCardProps {
  user: User;
  onEdit: (user: User) => void;
}

const UserCard: React.FC<UserCardProps> = ({ user, onEdit }) => {
  return (
    <div className="bg-card text-card-foreground p-4 rounded-lg">
      <h3 className="text-lg font-semibold">{user.fullName}</h3>
      <p className="text-muted-foreground">{user.email}</p>
      <button 
        onClick={() => onEdit(user)}
        className="mt-2 px-4 py-2 bg-primary text-primary-foreground rounded"
      >
        Edit
      </button>
    </div>
  );
};
```

### Testing Standards
- **Write tests** for new features and bug fixes
- **Maintain test coverage** above 80%
- **Use descriptive test names** that explain the scenario
- **Mock external dependencies** in unit tests
- **Write integration tests** for API endpoints

### Documentation Standards
- **Update README** for significant changes
- **Document API endpoints** with proper schemas
- **Add inline comments** for complex logic
- **Update environment templates** when adding new variables
- **Include migration instructions** for breaking changes

### Git Workflow
1. **Create feature branch** from `main`
2. **Make small, focused commits** with clear messages
3. **Rebase before merging** to maintain clean history
4. **Use conventional commit messages**:
   - `feat: add user authentication`
   - `fix: resolve dark mode styling issue`
   - `docs: update deployment instructions`
   - `test: add integration tests for auth API`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.