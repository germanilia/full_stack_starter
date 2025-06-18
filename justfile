# Install backend dependencies
install:
    cd backend && pip install -r requirements.txt
    cd client && npm install

# Initialize the database (create it if it doesn't exist)
init:
    cd backend && python -m app.db.init_db

# Generate a new Alembic migration with default message
generate-migration:
    cd backend && python -m app.db.generate_migration "Auto-generated migration"

# Apply Alembic migrations using config service for database connection
migrate:
    cd backend && python -m app.db.run_migrations

# Populate database with sample data
populate_db:
    cd backend && python -m app.db.populate_db

# Run the backend server
run-backend:
    cd backend && uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload

# Run the frontend client
run-client:
    cd client && npm start

# Run both backend and frontend
run:
    just run-backend & just run-client

# Database cleanup and setup helpers
cleanup-test-db:
    #!/bin/bash
    echo "🧹 Cleaning up test database..."
    # Remove SQLite test database if it exists
    if [ -f "backend/test_database.db" ]; then
        rm -f "backend/test_database.db"
        echo "✅ Removed SQLite test database"
    fi
    # For MySQL/PostgreSQL, we could add cleanup commands here
    echo "✅ Test database cleanup completed"

setup-test-db:
    #!/bin/bash
    echo "🔧 Setting up test database..."
    cd backend

    # Set test environment
    export APP_ENV=test

    # For SQLite (test environment), we need to create tables directly
    # since init_db.py has issues with SQLite database creation logic
    echo "📋 Creating database tables for test environment..."
    python -c "import os; os.environ['APP_ENV'] = 'test'; from app.db import engine; from app.models import Base; Base.metadata.create_all(bind=engine); print('✅ Database tables created successfully')"

    # Populate with test data
    echo "📊 Populating test database with test users..."
    APP_ENV=test python -m app.db.populate_test_db
    echo "✅ Test database setup completed"
    cd ..

# Backend test commands
test-backend-unit:
    #!/bin/bash
    echo "🧪 Running backend unit tests..."
    just cleanup-test-db
    just setup-test-db
    cd backend && python -m pytest tests/unit/ -v
    just cleanup-test-db

test-backend-integration:
    #!/bin/bash
    echo "🧪 Running backend integration tests..."
    just cleanup-test-db
    just setup-test-db
    cd backend && python -m pytest tests/integration/ -v
    just cleanup-test-db

test-backend:
    #!/bin/bash
    echo "🧪 Running all backend tests (unit + integration)..."
    just cleanup-test-db
    just setup-test-db
    cd backend && python -m pytest tests/ -v
    just cleanup-test-db

# UI test commands
test-ui-regression:
    #!/bin/bash
    echo "🧪 Running UI regression tests..."
    just cleanup-test-db
    just setup-test-db
    ./run-regression-tests.sh
    just cleanup-test-db

test-ui-full:
    #!/bin/bash
    echo "🧪 Running full UI test suite..."
    just cleanup-test-db
    just setup-test-db
    ./run-tests.sh
    just cleanup-test-db

# Combined test commands
test-full:
    #!/bin/bash
    echo "🚀 Running full test suite (backend + UI full)..."
    echo "📋 Test plan: Backend unit + integration + UI full suite"
    just cleanup-test-db
    just setup-test-db

    echo "🔧 Running backend tests..."
    cd backend && python -m pytest tests/ -v
    backend_result=$?
    cd ..

    if [ $backend_result -ne 0 ]; then
        echo "❌ Backend tests failed, skipping UI tests"
        just cleanup-test-db
        exit $backend_result
    fi

    echo "🌐 Running UI tests..."
    ./run-tests.sh
    ui_result=$?

    just cleanup-test-db

    if [ $ui_result -eq 0 ]; then
        echo "🎉 All tests passed!"
    else
        echo "❌ UI tests failed"
    fi

    exit $ui_result

# Legacy test commands (for backward compatibility)
test-backend-coverage:
    cd backend && python -m pytest --cov=app tests/

test-backend-verbose:
    cd backend && python -m pytest -v

test-ui:
    ./run-tests.sh

test-ui-clean:
    ./run-tests.sh clean

populate-test-db:
    cd backend && APP_ENV=test python -m app.db.populate_test_db

# Run all tests (legacy - use test-full instead)
test-all:
    just test-backend
    just test-ui

# SSH key management commands
ssh-use-germanilia:
    cp /tmp/host-germanilia-key ~/.ssh/id_rsa
    chmod 600 ~/.ssh/id_rsa
    echo "Now using germanilia SSH key"
    ssh-add -l

ssh-use-iliagerman:
    cp /tmp/host-iliagerman-key ~/.ssh/id_rsa
    chmod 600 ~/.ssh/id_rsa
    echo "Now using iliagerman SSH key"
    ssh-add -l

ssh-status:
    echo "Current SSH key fingerprint:"
    ssh-keygen -lf ~/.ssh/id_rsa
    echo "\nLoaded SSH keys:"
    ssh-add -l

git-test-connection:
    ssh -T git@github.com

# Create SQS queues in LocalStack
create_sqs:
    awslocal sqs create-queue --queue-name new-content
    awslocal sqs set-queue-attributes \
        --queue-url http://0.0.0.0:4566/000000000000/process-message-queue \
        --attributes '{ \
            "RedrivePolicy": "{\"deadLetterTargetArn\":\"arn:aws:sqs:us-east-1:000000000000:process-message-dead-letter-queue\",\"maxReceiveCount\":\"10\"}" \
        }'
    awslocal sqs set-queue-attributes \
        --queue-url http://0.0.0.0:4566/000000000000/new-content \
        --attributes '{ \
            "VisibilityTimeout": "10" \
        }'

# Purge all SQS queues in LocalStack
purge_sqs:
    awslocal sqs purge-queue --queue-url http://0.0.0.0:4566/000000000000/new-content --region=us-east-1

# Create Cognito User Pool and Client in AWS (only if they don't exist)
create_cognito:
    #!/bin/bash
    set -e

    # Change to backend directory to access configuration files
    cd backend

    # Load environment variables from .env file based on APP_ENV
    APP_ENV=${APP_ENV:-development}
    if [ -f ".env.$APP_ENV" ]; then
        export $(grep -v '^#' .env.$APP_ENV | xargs)
    fi

    # Load AWS credentials from secrets.yaml
    if [ -f "secrets.yaml" ]; then
        echo "Loading AWS credentials from secrets.yaml..."
        export AWS_ACCESS_KEY_ID=$(python3 -c "import yaml; data=yaml.safe_load(open('secrets.yaml')); print(data['aws']['access_key_id'])")
        export AWS_SECRET_ACCESS_KEY=$(python3 -c "import yaml; data=yaml.safe_load(open('secrets.yaml')); print(data['aws']['secret_access_key'])")
        export AWS_DEFAULT_REGION=$(python3 -c "import yaml; data=yaml.safe_load(open('secrets.yaml')); print(data['aws']['region'])")
        echo "✓ AWS credentials loaded successfully"
    else
        echo "Warning: secrets.yaml not found. Make sure AWS credentials are configured."
    fi

    # Use environment variables or defaults
    POOL_NAME=${COGNITO_POOL_NAME:-"MyAppUserPool"}
    CLIENT_NAME=${COGNITO_CLIENT_NAME:-"MyAppClient"}
    REGION=${COGNITO_REGION:-"us-east-1"}

    # Override AWS_DEFAULT_REGION with COGNITO_REGION if specified
    if [ -n "$COGNITO_REGION" ]; then
        export AWS_DEFAULT_REGION="$REGION"
        echo "Using Cognito region: $REGION"
    fi

    echo "Checking if Cognito User Pool exists in AWS..."

    # Try to find existing user pool by name
    EXISTING_POOL=$(aws cognito-idp list-user-pools --max-items 60 --region $REGION --query "UserPools[?Name=='$POOL_NAME'].Id" --output text 2>/dev/null || echo "")

    if [ -n "$EXISTING_POOL" ] && [ "$EXISTING_POOL" != "None" ]; then
        USER_POOL_ID="$EXISTING_POOL"
        echo "✓ User Pool already exists (ID: $USER_POOL_ID)"

        # Check if client exists
        EXISTING_CLIENT=$(aws cognito-idp list-user-pool-clients --user-pool-id "$USER_POOL_ID" --region $REGION --query "UserPoolClients[?ClientName=='$CLIENT_NAME'].ClientId" --output text 2>/dev/null || echo "")

        if [ -n "$EXISTING_CLIENT" ] && [ "$EXISTING_CLIENT" != "None" ]; then
            CLIENT_ID="$EXISTING_CLIENT"
            echo "✓ User Pool Client already exists (ID: $CLIENT_ID)"
            echo "Cognito resources are already set up!"
        else
            echo "User Pool exists but Client is missing. Creating Client..."
            # Create user pool client
            CLIENT_RESPONSE=$(aws cognito-idp create-user-pool-client \
                --user-pool-id "$USER_POOL_ID" \
                --client-name "$CLIENT_NAME" \
                --explicit-auth-flows "ALLOW_USER_PASSWORD_AUTH" "ALLOW_REFRESH_TOKEN_AUTH" "ALLOW_USER_SRP_AUTH" \
                --region $REGION \
                --query "UserPoolClient.ClientId" \
                --output text)
            CLIENT_ID="$CLIENT_RESPONSE"
            echo "✓ User Pool Client created successfully!"
        fi
    else
        echo "User Pool doesn't exist. Creating User Pool and Client..."

        # Create user pool with environment-specific configuration
        if [ "$APP_ENV" = "development" ]; then
            # Development: Simple setup, no email verification required
            echo "Creating development User Pool (no email verification)..."
            USER_POOL_RESPONSE=$(aws cognito-idp create-user-pool \
                --pool-name "$POOL_NAME" \
                --region $REGION \
                --policies '{"PasswordPolicy":{"MinimumLength":8,"RequireUppercase":false,"RequireLowercase":false,"RequireNumbers":false,"RequireSymbols":false}}' \
                --username-attributes email \
                --admin-create-user-config '{"AllowAdminCreateUserOnly":false}' \
                --query "UserPool.Id" \
                --output text)
        else
            # Production: Require email verification
            echo "Creating production User Pool (with email verification)..."
            USER_POOL_RESPONSE=$(aws cognito-idp create-user-pool \
                --pool-name "$POOL_NAME" \
                --region $REGION \
                --policies '{"PasswordPolicy":{"MinimumLength":8,"RequireUppercase":true,"RequireLowercase":true,"RequireNumbers":true,"RequireSymbols":false}}' \
                --username-attributes email \
                --admin-create-user-config '{"AllowAdminCreateUserOnly":false}' \
                --auto-verified-attributes email \
                --verification-message-template '{"DefaultEmailOption":"CONFIRM_WITH_CODE","EmailMessage":"Your verification code is {####}","EmailSubject":"Your verification code"}' \
                --query "UserPool.Id" \
                --output text)
        fi

        USER_POOL_ID="$USER_POOL_RESPONSE"
        echo "✓ User Pool created successfully! (ID: $USER_POOL_ID)"

        # Create user pool client
        CLIENT_RESPONSE=$(aws cognito-idp create-user-pool-client \
            --user-pool-id "$USER_POOL_ID" \
            --client-name "$CLIENT_NAME" \
            --explicit-auth-flows "ALLOW_USER_PASSWORD_AUTH" "ALLOW_REFRESH_TOKEN_AUTH" "ALLOW_USER_SRP_AUTH" \
            --region $REGION \
            --query "UserPoolClient.ClientId" \
            --output text)

        CLIENT_ID="$CLIENT_RESPONSE"
        echo "✓ User Pool Client created successfully!"
    fi

    echo ""
    echo "🎉 Cognito setup complete for environment: $APP_ENV"
    echo "User Pool Name: $POOL_NAME"
    echo "User Pool ID: $USER_POOL_ID"
    echo "Client Name: $CLIENT_NAME"
    echo "Client ID: $CLIENT_ID"
    echo "Region: $REGION"
    echo ""
    echo "💡 Note: This User Pool has minimal password requirements and no email verification for development ease."
    echo ""

    # Automatically add Cognito IDs to environment file
    echo "📝 Updating .env.$APP_ENV file..."
    if [ -f ".env.$APP_ENV" ]; then
        # Create a backup
        cp ".env.$APP_ENV" ".env.$APP_ENV.backup"

        # Remove any existing Cognito ID lines first (but keep COGNITO_REGION)
        grep -v "^COGNITO_USER_POOL_ID=" ".env.$APP_ENV" | grep -v "^COGNITO_CLIENT_ID=" | grep -v "^# Cognito IDs (from create_cognito" > ".env.$APP_ENV.tmp"
        mv ".env.$APP_ENV.tmp" ".env.$APP_ENV"

        # Add the new Cognito IDs
        echo "# Cognito IDs (from create_cognito_$APP_ENV output)" >> ".env.$APP_ENV"
        echo "COGNITO_USER_POOL_ID=$USER_POOL_ID" >> ".env.$APP_ENV"
        echo "COGNITO_CLIENT_ID=$CLIENT_ID" >> ".env.$APP_ENV"

        echo "✓ Added Cognito configuration to .env.$APP_ENV"
        echo "✓ Backup saved as .env.$APP_ENV.backup"
    else
        echo "⚠️  .env.$APP_ENV file not found. Please create it and add:"
        echo "COGNITO_USER_POOL_ID=$USER_POOL_ID"
        echo "COGNITO_CLIENT_ID=$CLIENT_ID"
        echo "COGNITO_REGION=$REGION"
    fi

    echo ""
    echo "🎉 Cognito setup complete! Your backend will automatically use the new configuration."

# Create Cognito for development environment
create_cognito_dev:
    APP_ENV=development just create_cognito

# Create Cognito for production environment
create_cognito_prod:
    APP_ENV=production just create_cognito

# Delete Cognito User Pool and Client
delete_cognito:
    #!/bin/bash
    set -e
    cd backend

    # Load environment variables
    APP_ENV=${APP_ENV:-development}
    if [ -f ".env.$APP_ENV" ]; then
        export $(grep -v '^#' .env.$APP_ENV | xargs)
    fi

    # Load AWS credentials from secrets.yaml
    if [ -f "secrets.yaml" ]; then
        echo "Loading AWS credentials from secrets.yaml..."
        export AWS_ACCESS_KEY_ID=$(python3 -c "import yaml; data=yaml.safe_load(open('secrets.yaml')); print(data['aws']['access_key_id'])")
        export AWS_SECRET_ACCESS_KEY=$(python3 -c "import yaml; data=yaml.safe_load(open('secrets.yaml')); print(data['aws']['secret_access_key'])")
        export AWS_DEFAULT_REGION=$(python3 -c "import yaml; data=yaml.safe_load(open('secrets.yaml')); print(data['aws']['region'])")
        echo "AWS credentials loaded successfully"
    fi

    # Get Cognito config from environment variables (not secrets.yaml)
    USER_POOL_ID=${COGNITO_USER_POOL_ID:-""}
    CLIENT_ID=${COGNITO_CLIENT_ID:-""}
    REGION=${COGNITO_REGION:-"us-east-1"}

    if [ -z "$USER_POOL_ID" ]; then
        echo "ERROR: COGNITO_USER_POOL_ID not found in environment variables"
        echo "Make sure .env.$APP_ENV contains COGNITO_USER_POOL_ID"
        exit 1
    fi

    echo "Deleting Cognito resources for environment: $APP_ENV"
    echo "User Pool ID: $USER_POOL_ID"
    echo "Client ID: $CLIENT_ID"
    echo "Region: $REGION"

    # Delete client if specified
    if [ -n "$CLIENT_ID" ]; then
        echo "Deleting User Pool Client: $CLIENT_ID"
        aws cognito-idp delete-user-pool-client --user-pool-id "$USER_POOL_ID" --client-id "$CLIENT_ID" --region "$REGION" || echo "Client deletion failed or already deleted"
    fi

    # Delete the user pool
    echo "Deleting User Pool: $USER_POOL_ID"
    aws cognito-idp delete-user-pool --user-pool-id "$USER_POOL_ID" --region "$REGION"

    # Remove Cognito IDs from environment file
    echo "Cleaning up environment variables..."
    if [ -f ".env.$APP_ENV" ]; then
        # Create a backup
        cp ".env.$APP_ENV" ".env.$APP_ENV.backup"

        # Remove the Cognito ID lines and related comments
        grep -v "^COGNITO_USER_POOL_ID=" ".env.$APP_ENV" | grep -v "^COGNITO_CLIENT_ID=" | grep -v "^# Cognito IDs (from create_cognito" > ".env.$APP_ENV.tmp"
        mv ".env.$APP_ENV.tmp" ".env.$APP_ENV"

        echo "Removed COGNITO_USER_POOL_ID and COGNITO_CLIENT_ID from .env.$APP_ENV"
        echo "Backup saved as .env.$APP_ENV.backup"
    fi

    echo "Cognito resources deleted successfully"

# Delete Cognito for development environment
delete_cognito_dev:
    APP_ENV=development just delete_cognito

# Delete Cognito for production environment
delete_cognito_prod:
    APP_ENV=production just delete_cognito

# Setup AWS services (LocalStack SQS + Real AWS Cognito)
setup_aws_services:
    just create_sqs
    just create_cognito

# Generate migration for Cognito fields
generate_cognito_migration:
    cd backend && python -m app.db.generate_cognito_migration