# Doctor Patient Management API

A backend application built using FastAPI for managing Doctors and Patients.

## Technologies Used

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- JWT Authentication
- Uvicorn
- Python-dotenv

## Features

- User registration
- User login
- JWT authentication
- Role-based authorization
- Admin and Doctor roles
- Doctor management
- Patient management
- Patient assignment to doctors
- Input validation
- Soft delete for doctors
- SQLite database


Setup
1. Create virtual environment
python -m venv venv

2. Activate virtual environment

Windows:

venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables

Create a .env file in the project root:

SECRET_KEY=my-super-secret-key-123456
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

5. Run the application
uvicorn app.main:app --reload

6. Open Swagger
http://127.0.0.1:8000/docs


## Authentication

1. Register a user using /auth/register.
2. Login using /auth/login.
3. The API returns a JWT access token.
4. Use the token in Swagger Authorize.
5. Protected APIs require authentication.
6. Admin-only APIs require the Admin role.

## Admin Role

Admin can:

- Create doctors
- View doctors
- Update doctors
- Delete doctors
- Create patients
- View patients
- Assign patients to doctors

## Doctor Role

Doctor can:

- Login
- View doctors
- View assigned patients

Doctors cannot access Admin-only patient management APIs.

## Doctor APIs

POST /doctors/ - Create Doctor - Admin only

GET /doctors/ - Get all Doctors - Authenticated users

GET /doctors/{doctor_id} - Get Doctor by ID - Authenticated users

PUT /doctors/{doctor_id} - Update Doctor - Admin only

DELETE /doctors/{doctor_id} - Delete Doctor - Admin only

POST /doctors/{doctor_id}/patients/{patient_id} - Assign Patient - Admin only

GET /doctors/{doctor_id}/patients - Get assigned Patients - Authenticated users

## Patient APIs

POST /patients/ - Create Patient - Admin only

GET /patients/ - Get all Patients - Admin only

GET /patients/{patient_id} - Get Patient by ID - Admin only

## Validation

- Doctor email must be valid and unique.
- Patient age must be greater than 0.
- Patient phone number must contain 10 to 15 digits.
- Invalid login returns 401 Unauthorized.
- Unauthorized role returns 403 Forbidden.
- Missing records return 404 Not Found.


## Database

SQLite is used for database persistence.

The application automatically creates the required database tables when the application starts.

## Assumptions

A patient is assigned to one doctor at a time using doctor_id.

The doctor user's username is matched with the doctor's email to identify the doctor account. This is a simplified implementation for the assignment.

## API Documentation

Swagger UI:

http://127.0.0.1:8000/docs



