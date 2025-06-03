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