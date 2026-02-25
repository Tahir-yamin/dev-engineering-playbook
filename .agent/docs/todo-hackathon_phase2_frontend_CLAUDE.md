# Frontend Development Guidelines

## Project Structure

This frontend is built with Next.js 14+ using the App Router. The structure is designed to be scalable and maintainable.

## Core Dependencies

- Next.js: React framework for production applications
- React: UI library
- React DOM: React package for DOM manipulation
- Axios: HTTP client for API requests
- Tailwind CSS: Utility-first CSS framework
- TypeScript: Type safety for JavaScript

## Development Guidelines

### File Structure
- `src/app/`: Next.js 14 App Router pages and layouts
- `src/components/`: Reusable React components
- `src/lib/`: Utility functions and API clients
- `src/hooks/`: Custom React hooks
- `src/types/`: TypeScript type definitions
- `src/styles/`: Global styles and Tailwind configuration

### API Integration
- All API calls should go through the centralized API client in `src/lib/api.ts`
- The API client handles authentication token management
- Response interceptors handle common error scenarios
- Use the proxy configuration in `next.config.js` to avoid CORS issues during development

### Environment Configuration
- Development: API requests are proxied to the backend (http://127.0.0.1:8000)
- Production: API requests go directly to the deployed backend

### Styling
- Use Tailwind CSS utility classes for styling
- Create reusable components with consistent styling
- Follow the design system for colors, spacing, and typography

## Component Architecture

### Naming Conventions
- Use PascalCase for component names
- Use camelCase for utility functions
- Use kebab-case for file names
- Use PascalCase for TypeScript interfaces and types

### State Management
- Use React hooks (useState, useEffect, etc.) for component-level state
- Consider using Context API for global state management
- For complex state management, consider libraries like Zustand

## API Client Usage

### Making Requests
- Import the API client: `import { api } from '@/lib/api';`
- Use the client for all backend communication
- The client automatically handles authentication headers

### Error Handling
- The API client includes response interceptors for common error handling
- 401 responses automatically redirect to login and clear the auth token
- Handle specific error cases as needed in components

## Development Workflow

### Local Development
- Run `npm run dev` to start the development server
- The proxy configuration allows API requests to reach the backend without CORS issues
- Changes to components are hot-reloaded

### Building for Production
- Run `npm run build` to create an optimized production build
- Run `npm run start` to serve the production build locally

## Security Considerations

### Authentication
- Authentication tokens are stored in localStorage (consider using httpOnly cookies in production)
- The API client automatically includes the auth token in requests
- Unauthorized responses trigger automatic logout

### Input Validation
- Validate user inputs both on the frontend and backend
- Use TypeScript to catch type-related errors at compile time
- Sanitize user inputs when appropriate

## Performance Optimization

### Code Splitting
- Next.js automatically handles code splitting by route
- Use dynamic imports for components that are not immediately needed

### Image Optimization
- Use Next.js Image component for optimized image delivery
- Implement lazy loading for images below the fold

## Testing Strategy

### Unit Tests
- Test individual components and utility functions
- Use Jest and React Testing Library

### Integration Tests
- Test API integration flows
- Mock API responses for consistent testing

## Deployment Considerations

### Environment Variables
- Use environment variables for API URLs and other configuration
- The proxy configuration in `next.config.js` should be updated for different environments

### Build Optimization
- Next.js provides automatic optimization for production builds
- Implement proper caching strategies
- Optimize images and assets