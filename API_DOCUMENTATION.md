# Nexus API Documentation

## Base URL
```
http://127.0.0.1:5001
```

---

## Authentication Endpoints (`/auth`)

### 1. Register New User
**Endpoint:** `POST /auth/register`  
**Authentication:** Not required  
**Role:** Public  

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "role": "employee",
  "first_name": "John",
  "last_name": "Doe",
  "address": "123 Main St",
  "department": "Engineering"
}
```

**Required Fields:**
- `email` (valid email format)
- `password` (min 8 chars, at least 1 letter and 1 number)

**Optional Fields:**
- `role` (default: "employee", options: "hr", "manager", "employee")
- `first_name`, `last_name`, `address`, `department`

**Response (201 Created):**
```json
{
  "status": 201,
  "message": "Account created successfully",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "role": "employee",
    "first_name": "John",
    "last_name": "Doe",
    "department": "Engineering",
    "manager_id": null,
    "created_at": "2025-11-14T10:30:00"
  }
}
```

---

### 2. Login
**Endpoint:** `POST /auth/login`  
**Authentication:** Not required  
**Role:** Public  

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "role": "employee",
      "first_name": "John",
      "last_name": "Doe",
      "department": "Engineering",
      "manager_id": null,
      "created_at": "2025-11-14T10:30:00"
    }
  }
}
```

---

## User Management Endpoints (`/users`)

### 3. Get All Users
**Endpoint:** `GET /users/`  
**Authentication:** Required (JWT token)  
**Role:** All authenticated users  

**Headers:**
```
Authorization: Bearer <access_token>
```

**Access Control:**
- **HR:** Can see all users
- **Manager:** Can see themselves + their team members
- **Employee:** Can see only themselves

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "Users retrieved successfully",
  "data": [
    {
      "id": 1,
      "email": "user@example.com",
      "role": "employee",
      "first_name": "John",
      "last_name": "Doe",
      "department": "Engineering",
      "manager_id": 2,
      "created_at": "2025-11-14T10:30:00"
    }
  ]
}
```

---

### 4. Get User by ID
**Endpoint:** `GET /users/<user_id>`  
**Authentication:** Required (JWT token)  
**Role:** HR, Manager (for their team), User (for themselves)  

**Headers:**
```
Authorization: Bearer <access_token>
```

**Example:** `GET /users/5`

**Access Control:**
- **HR:** Can view any user
- **Manager:** Can view themselves and their team members
- **Employee:** Can view only themselves

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "User retrieved successfully",
  "data": {
    "id": 5,
    "email": "user@example.com",
    "role": "employee",
    "first_name": "John",
    "last_name": "Doe",
    "department": "Engineering",
    "manager_id": 2,
    "created_at": "2025-11-14T10:30:00",
    "address": "123 Main St",
    "date_of_birth": "1990-05-15"
  }
}
```

---

### 5. Get Current User Profile
**Endpoint:** `GET /users/me`  
**Authentication:** Required (JWT token)  
**Role:** All authenticated users  

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "Current user retrieved successfully",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "role": "employee",
    "first_name": "John",
    "last_name": "Doe",
    "department": "Engineering",
    "manager_id": 2,
    "created_at": "2025-11-14T10:30:00",
    "address": "123 Main St",
    "date_of_birth": "1990-05-15"
  }
}
```

---

### 6. Update User by ID
**Endpoint:** `PUT /users/<user_id>`  
**Authentication:** Required (JWT token)  
**Role:** HR (all fields), User (limited fields for themselves)  

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Example:** `PUT /users/5`

**Request Body (HR - all fields):**
```json
{
  "email": "newemail@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "role": "manager",
  "department": "Sales",
  "manager_id": 3,
  "address": "456 Oak Ave",
  "password": "NewPass456"
}
```

**Request Body (Employee - own profile):**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "address": "456 Oak Ave",
  "password": "NewPass456"
}
```

**Fields:**
- **HR can update:** email, role, first_name, last_name, department, manager_id, address, password
- **User can update (own profile):** first_name, last_name, address, password

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "User updated successfully",
  "data": {
    "id": 5,
    "email": "newemail@example.com",
    "role": "manager",
    "first_name": "Jane",
    "last_name": "Smith",
    "department": "Sales",
    "manager_id": 3,
    "created_at": "2025-11-14T10:30:00"
  }
}
```

---

### 7. Update Current User Profile
**Endpoint:** `PUT /users/me`  
**Authentication:** Required (JWT token)  
**Role:** All authenticated users  

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "address": "456 Oak Ave",
  "password": "NewPass456"
}
```

**Allowed Fields:**
- `first_name`, `last_name`, `address`, `password`

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "Profile updated successfully",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "role": "employee",
    "first_name": "Jane",
    "last_name": "Smith",
    "department": "Engineering",
    "manager_id": 2,
    "created_at": "2025-11-14T10:30:00",
    "address": "456 Oak Ave",
    "date_of_birth": "1990-05-15"
  }
}
```

---

### 8. Delete User
**Endpoint:** `DELETE /users/<user_id>`  
**Authentication:** Required (JWT token)  
**Role:** HR only  

**Headers:**
```
Authorization: Bearer <access_token>
```

**Example:** `DELETE /users/5`

**Note:** Cannot delete your own account

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "User deleted successfully"
}
```

---

## HR Management Endpoints (`/hr`)

### 9. Create Employee
**Endpoint:** `POST /hr/employees`  
**Authentication:** Required (JWT token)  
**Role:** HR only  

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "employee@example.com",
  "password": "SecurePass123",
  "first_name": "Alice",
  "last_name": "Johnson",
  "department": "Marketing",
  "manager_id": 3
}
```

**Required Fields:**
- `email`, `password`

**Optional Fields:**
- `first_name`, `last_name`, `department`, `manager_id`

**Response (201 Created):**
```json
{
  "status": 201,
  "message": "Employee created successfully",
  "data": {
    "id": 10,
    "email": "employee@example.com",
    "role": "employee",
    "first_name": "Alice",
    "last_name": "Johnson",
    "department": "Marketing",
    "manager_id": 3,
    "created_at": "2025-11-14T11:00:00"
  }
}
```

---

### 10. Get Employees List
**Endpoint:** `GET /hr/employees`  
**Authentication:** Required (JWT token)  
**Role:** HR, Manager  

**Headers:**
```
Authorization: Bearer <access_token>
```

**Access Control:**
- **HR:** Can see all employees
- **Manager:** Can see only their direct reports

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "Employees retrieved successfully",
  "data": [
    {
      "id": 10,
      "email": "employee@example.com",
      "role": "employee",
      "first_name": "Alice",
      "last_name": "Johnson",
      "department": "Marketing",
      "manager_id": 3,
      "created_at": "2025-11-14T11:00:00"
    }
  ]
}
```

---

### 11. Get Employee by ID
**Endpoint:** `GET /hr/employees/<employee_id>`  
**Authentication:** Required (JWT token)  
**Role:** HR, Manager (for their team)  

**Headers:**
```
Authorization: Bearer <access_token>
```

**Example:** `GET /hr/employees/10`

**Access Control:**
- **HR:** Can view any employee
- **Manager:** Can view only their team members

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "Employee retrieved successfully",
  "data": {
    "id": 10,
    "email": "employee@example.com",
    "role": "employee",
    "first_name": "Alice",
    "last_name": "Johnson",
    "department": "Marketing",
    "manager_id": 3,
    "created_at": "2025-11-14T11:00:00",
    "address": "789 Pine Rd",
    "date_of_birth": "1995-08-20"
  }
}
```

---

### 12. Update Employee
**Endpoint:** `PUT /hr/employees/<employee_id>`  
**Authentication:** Required (JWT token)  
**Role:** HR only  

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Example:** `PUT /hr/employees/10`

**Request Body:**
```json
{
  "first_name": "Alicia",
  "last_name": "Johnson",
  "department": "Sales",
  "manager_id": 5
}
```

**Allowed Fields:**
- `first_name`, `last_name`, `department`, `manager_id`

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "Employee updated successfully",
  "data": {
    "id": 10,
    "email": "employee@example.com",
    "role": "employee",
    "first_name": "Alicia",
    "last_name": "Johnson",
    "department": "Sales",
    "manager_id": 5,
    "created_at": "2025-11-14T11:00:00"
  }
}
```

---

### 13. Delete Employee
**Endpoint:** `DELETE /hr/employees/<employee_id>`  
**Authentication:** Required (JWT token)  
**Role:** HR only  

**Headers:**
```
Authorization: Bearer <access_token>
```

**Example:** `DELETE /hr/employees/10`

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "Employee deleted successfully"
}
```

---

## Health Check Endpoints

### 14. API Status
**Endpoint:** `GET /`  
**Authentication:** Not required  
**Role:** Public  

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "Nexus API is running",
  "version": "2.0"
}
```

---

### 15. Health Check
**Endpoint:** `GET /health`  
**Authentication:** Not required  
**Role:** Public  

**Response (200 OK):**
```json
{
  "status": 200,
  "message": "OK"
}
```

---

## Common Error Responses

### 400 Bad Request
```json
{
  "status": 400,
  "message": "Email and password are required"
}
```

### 401 Unauthorized
```json
{
  "status": 401,
  "message": "Invalid email or password"
}
```

### 403 Forbidden
```json
{
  "status": 403,
  "message": "Access denied. Required role(s): hr"
}
```

### 404 Not Found
```json
{
  "status": 404,
  "message": "User not found"
}
```

### 409 Conflict
```json
{
  "status": 409,
  "message": "Email already registered"
}
```

### 500 Internal Server Error
```json
{
  "status": 500,
  "message": "Internal server error"
}
```

---

## Role-Based Access Summary

| Endpoint | Public | Employee | Manager | HR |
|----------|--------|----------|---------|-----|
| POST /auth/register | ✅ | ✅ | ✅ | ✅ |
| POST /auth/login | ✅ | ✅ | ✅ | ✅ |
| GET /users/ | ❌ | ✅ (self) | ✅ (team) | ✅ (all) |
| GET /users/:id | ❌ | ✅ (self) | ✅ (team) | ✅ (all) |
| GET /users/me | ❌ | ✅ | ✅ | ✅ |
| PUT /users/:id | ❌ | ✅ (self, limited) | ❌ | ✅ (all) |
| PUT /users/me | ❌ | ✅ | ✅ | ✅ |
| DELETE /users/:id | ❌ | ❌ | ❌ | ✅ |
| POST /hr/employees | ❌ | ❌ | ❌ | ✅ |
| GET /hr/employees | ❌ | ❌ | ✅ (team) | ✅ (all) |
| GET /hr/employees/:id | ❌ | ❌ | ✅ (team) | ✅ (all) |
| PUT /hr/employees/:id | ❌ | ❌ | ❌ | ✅ |
| DELETE /hr/employees/:id | ❌ | ❌ | ❌ | ✅ |
| GET / | ✅ | ✅ | ✅ | ✅ |
| GET /health | ✅ | ✅ | ✅ | ✅ |

---

## Password Requirements
- Minimum 8 characters
- At least 1 letter
- At least 1 number

## Email Requirements
- Must be valid email format
- Must be unique across all users

---

## Example Usage (cURL)

### Register a new user:
```bash
curl -X POST http://127.0.0.1:5001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"Pass1234","first_name":"John","last_name":"Doe"}'
```

### Login:
```bash
curl -X POST http://127.0.0.1:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"Pass1234"}'
```

### Get current user profile:
```bash
curl -X GET http://127.0.0.1:5001/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update current user profile:
```bash
curl -X PUT http://127.0.0.1:5001/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jane","last_name":"Smith"}'
```

### Get all users (HR only):
```bash
curl -X GET http://127.0.0.1:5001/users/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Delete user (HR only):
```bash
curl -X DELETE http://127.0.0.1:5001/users/5 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
