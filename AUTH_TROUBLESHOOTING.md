# Troubleshooting Authentication Issues

## Common Error Codes and Solutions

### 401 Unauthorized (Signin)
- **Cause**: Invalid email/password combination or expired/invalid token
- **Solution**: 
  - Verify the email and password are correct
  - Ensure you're sending credentials in the correct format:
    ```json
    {
      "email": "user@example.com",
      "password": "SecurePassword123!"
    }
    ```

### 422 Unprocessable Content (Signup)
- **Cause**: Invalid request format or validation errors
- **Solution**:
  - Ensure all required fields are provided: `email`, `password`
  - Password must be at least 8 characters long
  - Email must be in valid format
  - Request must be sent as JSON with correct Content-Type header

### 409 Conflict (Signup)
- **Cause**: Email already registered
- **Solution**: Use a different email address or sign in instead of signing up

## Correct API Usage

### Sign Up
```bash
POST /api/v1/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "name": "User Name"
}
```

### Sign In
```bash
POST /api/v1/auth/signin
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

### Accessing Protected Endpoints
```bash
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

## Common Mistakes to Avoid

1. **Not running the server**: Make sure the backend server is running on the correct port (default: 8001)
2. **Wrong Content-Type**: Always send requests with `Content-Type: application/json`
3. **Missing fields**: Ensure all required fields are included in the request body
4. **Invalid email format**: Emails must follow standard format (e.g., user@example.com)
5. **Weak passwords**: Passwords must be at least 8 characters long
6. **Incorrect authorization header**: Use `Bearer <token>` format for protected endpoints

## Verification Steps

If you're experiencing issues, verify:

1. Server is running: `curl http://localhost:8001/`
2. Database is accessible and tables are created
3. Environment variables are set correctly (especially `BETTER_AUTH_SECRET`)
4. Request format matches the expected schema

## Testing Scripts

Use the following scripts to verify authentication functionality:

- `verify_auth_fix_ascii.py` - Comprehensive authentication verification
- `demo_auth_usage.py` - Demonstration of correct API usage