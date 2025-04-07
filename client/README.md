# Client Application

This is the frontend for the My Boilerplate App, built with React, TypeScript, and Vite.

## Environment Configuration

The application uses environment variables for configuration. These are loaded by Vite during the build process.

### Available Environment Variables

- `VITE_API_URL`: The URL of the backend API

### Environment Files

The application uses different environment files for different environments:

- `.env.development`: Used during development (`npm run dev`)
- `.env.production`: Used for production builds (`npm run build`)

### Adding New Environment Variables

1. Add the variable to the appropriate `.env` files
2. Add the variable type to `src/vite-env.d.ts`
3. Add the variable to the `AppConfig` interface in `src/lib/config.ts`
4. Add a getter function in `config.ts` to load the variable

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

- `src/`: Source code
  - `components/`: React components
  - `lib/`: Utility functions and services
    - `api.ts`: API client for communicating with the backend
    - `config.ts`: Configuration service
  - `App.tsx`: Main application component
  - `main.tsx`: Application entry point
