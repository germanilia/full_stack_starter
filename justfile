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

# Create Cognito User Pool and Client in LocalStack
create_cognito:
    #!/bin/bash
    echo "Creating Cognito User Pool in LocalStack..."

    # Create user pool with predefined ID
    awslocal cognito-idp create-user-pool \
        --pool-name "MyAppUserPool" \
        --user-pool-tags "_custom_id_=us-east-1_myid123" \
        --policies '{"PasswordPolicy":{"MinimumLength":8,"RequireUppercase":true,"RequireLowercase":true,"RequireNumbers":true,"RequireSymbols":false}}' \
        --auto-verified-attributes email \
        --username-attributes email \
        --verification-message-template '{"DefaultEmailOption":"CONFIRM_WITH_CODE"}' \
        --admin-create-user-config '{"AllowAdminCreateUserOnly":false}'

    # Create user pool client with predefined ID
    awslocal cognito-idp create-user-pool-client \
        --user-pool-id "us-east-1_myid123" \
        --client-name "_custom_id_:myclient123" \
        --generate-secret \
        --explicit-auth-flows "USER_PASSWORD_AUTH" "REFRESH_TOKEN_AUTH" \
        --supported-identity-providers "COGNITO" \
        --read-attributes "email" "name" \
        --write-attributes "email" "name"

    echo "Cognito User Pool and Client created successfully!"
    echo "User Pool ID: us-east-1_myid123"
    echo "Client ID: myclient123"

# Setup LocalStack services (SQS + Cognito)
setup_localstack:
    just create_sqs
    just create_cognito

# Generate migration for Cognito fields
generate_cognito_migration:
    cd backend && python -m app.db.generate_cognito_migration