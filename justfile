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

# Create Cognito User Pool and Client in LocalStack (only if they don't exist)
create_cognito:
    #!/bin/bash
    set -e

    USER_POOL_ID="us-east-1_myid123"
    CLIENT_ID="myclient123"
    POOL_NAME="MyAppUserPool"

    echo "Checking if Cognito User Pool exists in LocalStack..."

    # Check if user pool exists
    if awslocal cognito-idp describe-user-pool --user-pool-id "$USER_POOL_ID" >/dev/null 2>&1; then
        echo "✓ User Pool already exists (ID: $USER_POOL_ID)"

        # Check if client exists
        if awslocal cognito-idp describe-user-pool-client --user-pool-id "$USER_POOL_ID" --client-id "$CLIENT_ID" >/dev/null 2>&1; then
            echo "✓ User Pool Client already exists (ID: $CLIENT_ID)"
            echo "Cognito resources are already set up!"
            exit 0
        else
            echo "User Pool exists but Client is missing. Creating Client..."
            # Create user pool client with predefined ID
            awslocal cognito-idp create-user-pool-client \
                --user-pool-id "$USER_POOL_ID" \
                --client-name "_custom_id_:$CLIENT_ID" \
                --generate-secret \
                --explicit-auth-flows "USER_PASSWORD_AUTH" "REFRESH_TOKEN_AUTH" \
                --supported-identity-providers "COGNITO" \
                --read-attributes "email" "name" \
                --write-attributes "email" "name"
            echo "✓ User Pool Client created successfully!"
        fi
    else
        echo "User Pool doesn't exist. Creating User Pool and Client..."

        # Create user pool with predefined ID
        awslocal cognito-idp create-user-pool \
            --pool-name "$POOL_NAME" \
            --user-pool-tags "_custom_id_=$USER_POOL_ID" \
            --policies '{"PasswordPolicy":{"MinimumLength":8,"RequireUppercase":true,"RequireLowercase":true,"RequireNumbers":true,"RequireSymbols":false}}' \
            --auto-verified-attributes email \
            --username-attributes email \
            --verification-message-template '{"DefaultEmailOption":"CONFIRM_WITH_CODE"}' \
            --admin-create-user-config '{"AllowAdminCreateUserOnly":false}'

        echo "✓ User Pool created successfully!"

        # Create user pool client with predefined ID
        awslocal cognito-idp create-user-pool-client \
            --user-pool-id "$USER_POOL_ID" \
            --client-name "_custom_id_:$CLIENT_ID" \
            --generate-secret \
            --explicit-auth-flows "USER_PASSWORD_AUTH" "REFRESH_TOKEN_AUTH" \
            --supported-identity-providers "COGNITO" \
            --read-attributes "email" "name" \
            --write-attributes "email" "name"

        echo "✓ User Pool Client created successfully!"
    fi

    echo ""
    echo "🎉 Cognito setup complete!"
    echo "User Pool ID: $USER_POOL_ID"
    echo "Client ID: $CLIENT_ID"

# Setup LocalStack services (SQS + Cognito)
setup_localstack:
    just create_sqs
    just create_cognito

# Generate migration for Cognito fields
generate_cognito_migration:
    cd backend && python -m app.db.generate_cognito_migration