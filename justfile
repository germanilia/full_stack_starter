# Install backend dependencies
install:
    cd backend && pip install -r requirements.txt
    cd client && npm install

# Run the backend server
run-backend:
    cd backend && uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload

# Generate a new Alembic migration script
migrate-generate message='':
    cd backend && alembic revision --autogenerate -m "{{message}}"

# Apply Alembic migrations
migrate-run:
    cd backend && alembic upgrade head

run-client:
    cd client && npm start

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