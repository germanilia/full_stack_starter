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

# Test commands
test-backend:
    cd backend && python -m pytest

test-backend-unit:
    cd backend && python -m pytest tests/unit/

test-backend-integration:
    cd backend && python -m pytest tests/integration/

test-backend-coverage:
    cd backend && python -m pytest --cov=app tests/

test-backend-verbose:
    cd backend && python -m pytest -v

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

        # Create user pool with auto-confirmation (no email verification)
        USER_POOL_RESPONSE=$(aws cognito-idp create-user-pool \
            --pool-name "$POOL_NAME" \
            --region $REGION \
            --policies '{"PasswordPolicy":{"MinimumLength":8,"RequireUppercase":false,"RequireLowercase":false,"RequireNumbers":false,"RequireSymbols":false}}' \
            --username-attributes email \
            --admin-create-user-config '{"AllowAdminCreateUserOnly":false}' \
            --query "UserPool.Id" \
            --output text)

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
    echo "📝 Next steps:"
    echo "1. Update your application configuration with these values"
    echo "2. If using AWS Secrets Manager, add these to your secret"
    echo "3. For local development, you can add these to your secrets.yaml file:"
    echo ""
    echo "cognito:"
    echo "  user_pool_id: \"$USER_POOL_ID\""
    echo "  client_id: \"$CLIENT_ID\""
    echo "  region: \"$REGION\""

# Create Cognito for development environment
create_cognito_dev:
    APP_ENV=development just create_cognito

# Create Cognito for production environment
create_cognito_prod:
    APP_ENV=production just create_cognito

# Setup AWS services (LocalStack SQS + Real AWS Cognito)
setup_aws_services:
    just create_sqs
    just create_cognito

# Generate migration for Cognito fields
generate_cognito_migration:
    cd backend && python -m app.db.generate_cognito_migration