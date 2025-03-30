# My Boilerplate App

This project is a boilerplate for building applications using FastAPI for the backend and React for the frontend. It includes essential tools and configurations to get started quickly.

## Project Structure

```
my-boilerplate-app
├── backend
│   ├── alembic
│   │   ├── versions
│   │   └── env.py
│   ├── app
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routers
│   │   │   └── __init__.py
│   │   ├── models
│   │   │   └── __init__.py
│   │   ├── crud
│   │   │   └── __init__.py
│   │   ├── db
│   │   │   └── __init__.py
│   │   └── core
│   │       ├── __init__.py
│   │       └── config.py
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example # Note: This is now deprecated, use root .env.example
├── client
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── App.js
│   │   ├── index.js
│   │   └── components
│   │       └── ui
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── Dockerfile
├── .vscode
│   └── launch.json
├── .env
├── .env.example # Use this for environment variable setup
├── .gitignore # Project-wide git ignore file
├── docker-compose.yml
├── justfile
└── README.md
```

## Backend

The backend is built using FastAPI and includes:

- **Alembic** for database migrations.
- **Pydantic** for data validation.
- **PostgreSQL** as the database.
- General logging capabilities.
- Environment variables management through a root `.env` file.

### Requirements

To install the backend dependencies, run:

```bash
just install
```

### Running the Backend

To run the backend application, use:

```bash
just run
```

### Database Migrations

This project uses Alembic to manage database schema migrations. Ensure you have configured your `.env` file with the correct `DATABASE_URL`.

**Generating Migrations:**

After making changes to your SQLAlchemy models (in `backend/app/models/`), generate a new migration script:

```bash
just migrate-generate message="Your descriptive migration message"
```

Replace `"Your descriptive migration message"` with a short description of the changes. This will create a new file in `backend/alembic/versions/`.

**Running Migrations:**

To apply the migrations to your database:

```bash
just migrate-run
```

This command applies all pending migrations.

## Client

The client is built using React and includes:

- **shadcn/ui** for UI components.
- **Tailwind CSS** for styling.

### Requirements

To install the client dependencies, navigate to the client directory and run:

```bash
cd client
npm install
```

### Running the Client

To run the client application, navigate to the client directory and use:

```bash
cd client
npm start
```

### Adding UI Components (shadcn/ui)

To add new UI components from shadcn/ui, navigate to the `client` directory and use the `npx shadcn add` command followed by the component names:

```bash
cd client
npx shadcn add [component-name] [another-component-name]
```

For example, to add `table`, `card`, `badge`, and `button` components:

```bash
npx shadcn add table card badge button input select command
```

This will add the necessary files to your `client/src/components/ui` directory.

## Docker

This project includes Docker configurations for both the backend and client. To build and run the containers, use:

```bash
docker-compose up --build
```

## Environment Variables

Make sure to create a `.env` file in the **root directory** of the project. You can copy the `.env.example` file located in the root directory to get started:

```bash
cp .env.example .env
```

Edit the `.env` file to include all necessary environment variables. The `DATABASE_URL` is constructed from `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `DB_HOST`, and `DB_PORT`. Ensure these are set correctly for your environment (Docker or local development). Alembic and the FastAPI application are configured to read variables from this root `.env` file.

## Git Ignore

A `.gitignore` file is included in the root directory to exclude common temporary files, environment files, and build artifacts from version control.

## VS Code Configuration

The project includes a `.vscode` directory with a launch configuration (`launch.json`) to potentially run and debug components.

## License

This project is licensed under the MIT License.