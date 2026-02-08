# Implementation Plan: Authentication System

**Branch**: `005-authentication-system` | **Date**: 2026-02-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-authentication-system/spec.md`

## Summary

Implement JWT-based authentication system with user registration, login, and token validation. Use bcrypt for password hashing and PyJWT for token generation. Implement JWTBearer middleware to protect API endpoints.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: bcrypt, PyJWT, FastAPI
**Storage**: PostgreSQL (User table from 003-database-schema)
**Testing**: Manual testing with curl/Postman
**Target Platform**: Linux/Windows server
**Project Type**: Web application (backend)
**Performance Goals**: < 200ms authentication response time
**Constraints**: JWT tokens expire in 30 minutes, bcrypt hashing required
**Scale/Scope**: Support 1000+ users, 10000+ auth requests/day

## Constitution Check

✅ **PASS**: Spec-Driven Development followed
✅ **PASS**: JWT authentication as mandated
✅ **PASS**: Better Auth secret integration
✅ **PASS**: Password hashing with bcrypt
✅ **PASS**: No localStorage for tokens (handled by frontend)

## Project Structure

### Documentation (this feature)

```text
specs/005-authentication-system/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Task breakdown
```

### Source Code (repository root)

```text
src/backend/app/
├── auth/
│   ├── router.py        # Auth endpoints (register, login, logout)
│   ├── service.py       # Auth business logic (create_user, authenticate, token generation)
│   └── middleware.py    # JWTBearer middleware for token validation
├── models.py            # User, UserRegistration, UserLogin, Token models (already exists)
├── database.py          # Database session (already exists)
└── main.py              # FastAPI app with auth router registration
```

**Structure Decision**: Separate auth module with router, service, and middleware. Service layer handles business logic, middleware handles token validation.

## Authentication Flow

### Registration Flow

1. Client sends POST /api/auth/register with email and password
2. Backend checks if email already exists
3. Backend hashes password with bcrypt
4. Backend creates User record in database
5. Backend generates JWT token with user_id and email
6. Backend returns token to client

### Login Flow

1. Client sends POST /api/auth/login with email and password
2. Backend queries User by email
3. Backend verifies password with bcrypt.checkpw()
4. Backend updates last_login_at timestamp
5. Backend generates JWT token with user_id and email
6. Backend returns token to client

### Token Validation Flow

1. Client sends request with Authorization: Bearer <token> header
2. JWTBearer middleware extracts token from header
3. Middleware verifies token signature with BETTER_AUTH_SECRET
4. Middleware checks token expiration
5. Middleware extracts user_id from payload
6. Middleware sets request.state.user_id for route handlers
7. Route handler proceeds with authenticated user_id

## JWT Token Structure

```json
{
  "sub": "user@example.com",
  "user_id": "uuid-string",
  "exp": 1234567890
}
```

**Algorithm**: HS256
**Secret**: BETTER_AUTH_SECRET environment variable
**Expiration**: 30 minutes from creation

## Password Security

**Hashing Algorithm**: bcrypt
**Salt Rounds**: Default (12 rounds)
**Storage**: Hashed password stored in User.password field
**Verification**: bcrypt.checkpw() for login validation

## API Endpoints Design

### POST /api/auth/register
- **Request Body**: `UserRegistration` (email, password)
- **Response**: `Token` (access_token, token_type)
- **Status Codes**: 201 Created, 400 Bad Request, 422 Validation Error, 500 Internal Server Error

### POST /api/auth/login
- **Request Body**: `UserLogin` (email, password)
- **Response**: `Token` (access_token, token_type)
- **Status Codes**: 200 OK, 401 Unauthorized, 422 Validation Error

### POST /api/auth/logout
- **Request Body**: None
- **Response**: `{"message": "Successfully logged out"}`
- **Status Codes**: 200 OK
- **Note**: Stateless JWT, actual logout is client-side token removal

## Middleware Implementation

**JWTBearer Class**:
- Extends FastAPI's HTTPBearer
- Validates Authorization header format
- Verifies JWT token signature and expiration
- Extracts user_id from token payload
- Sets request.state.user_id for route handlers
- Raises HTTPException(401) on validation failure

## Error Handling

**400 Bad Request**: User already exists (registration)
**401 Unauthorized**: Invalid credentials, invalid/expired token
**422 Validation Error**: Invalid email format, weak password
**500 Internal Server Error**: Database errors, token generation failures

## Environment Variables

**BETTER_AUTH_SECRET**: JWT signing secret (min 32 chars)
**Default**: "your-secret-key-change-in-production" (with warning)

## Security Considerations

- Passwords never logged or exposed in responses
- Authentication errors don't reveal if email exists (generic "Invalid credentials")
- JWT secret loaded from environment (never hardcoded)
- Token expiration enforced to limit exposure window
- bcrypt hashing prevents rainbow table attacks

## Integration Points

**Database**: Uses User model from 003-database-schema
**API Endpoints**: Protected by JWTBearer middleware from this feature
**Frontend**: Receives tokens and includes in Authorization header

## Acceptance Criteria

- [ ] User registration creates user with hashed password
- [ ] User login validates credentials and returns JWT token
- [ ] JWT tokens contain user_id and email in payload
- [ ] JWTBearer middleware validates tokens on protected endpoints
- [ ] Invalid tokens return 401 Unauthorized
- [ ] Expired tokens return 401 Unauthorized
- [ ] Passwords are never stored in plain text
- [ ] Auth router registered in main.py with /api/auth prefix
