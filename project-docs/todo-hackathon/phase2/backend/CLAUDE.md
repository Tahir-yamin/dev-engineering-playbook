# Backend Development Guidelines

## Project Structure

This backend is built with FastAPI and SQLModel for the Todo application. The structure is designed to be scalable and maintainable.

## Core Components

### Dependencies
- FastAPI: Modern, fast web framework for building APIs
- SQLModel: Combines SQLAlchemy and Pydantic for type-safe database models
- Uvicorn: ASGI server for running the application
- Python-Jose: For JWT token handling and authentication
- Passlib: For password hashing

### Database Configuration
- Uses SQLite for local development (file-based)
- Structured to easily switch to Neon DB (PostgreSQL) in production
- Connection pooling and async support ready
- Environment variable for DATABASE_URL

### Models
- User and Task models defined with proper relationships
- Base, Create, Update, and Public model variants
- Proper validation and constraints
- UUID primary keys for better security

## Development Guidelines

### Adding New Features
1. Create new models in models.py following the existing pattern
2. Create database operations in separate files (e.g., crud.py)
3. Add API routes in separate route files (e.g., routes/tasks.py)
4. Import and include new routes in main.py

### Environment Variables
- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `SECRET_KEY`: Secret key for JWT tokens
- `ALGORITHM`: Algorithm for JWT encoding (e.g., HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Security Practices
- Always validate input using Pydantic models
- Use dependency injection for authentication checks
- Hash passwords using passlib/bcrypt
- Implement proper error handling
- Use CORS middleware appropriately

## API Design Principles

### Response Format
- Consistent structure for success and error responses
- Use Pydantic models for request/response validation
- Proper HTTP status codes

### Error Handling
- Use HTTPException for standard HTTP errors
- Custom exception handlers where needed
- Proper logging of errors

## Deployment Considerations

### Local Development
- Use `uvicorn main:app --reload` for development
- SQLite database stored as file in project directory

### Production Deployment
- Switch DATABASE_URL to Neon DB connection string
- Use proper process manager (e.g., gunicorn with uvicorn workers)
- Set up proper logging
- Implement monitoring and health checks

## Testing Strategy

### Unit Tests
- Test model validations
- Test database operations (CRUD)
- Test utility functions

### Integration Tests
- Test API endpoints
- Test authentication flows
- Test database transactions

## Future Enhancements

### Database Migrations
- Alembic integration for schema migrations
- Proper migration scripts for production deployments

### Performance
- Caching layer implementation
- Query optimization
- Connection pooling configuration

### Monitoring
- Metrics collection
- Request tracing
- Error tracking