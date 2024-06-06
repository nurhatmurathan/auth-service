# FastAPI Authentication Service

This is a FastAPI-based authentication service that provides JWT authentication with features for token refresh and verification. This service can be integrated into any application requiring user authentication.

## Features

- **JWT Authentication**: Secure token-based authentication.
- **Refresh Tokens**: Support for refreshing access tokens.
- **Token Verification**: Endpoint to verify tokens.
- **User Registration and Login**: Register new users and authenticate existing ones.

## Getting Started

### Prerequisites

- Python 3.7+
- FastAPI
- SQLAlchemy
- Passlib
- PyJWT
- PostgreSQL

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
    ```
   
2. **Create a virtual environment:**:
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
   
3. **Install dependencies:**:
   ```bash
    pip install -r requirements.txt
    ```
### Configuration

Create a .env file in the root directory with the following environment variables:
```env
DB_HOST="localhost"
DB_USER="nurha"
DB_PASS="8996"
DB_NAME="nurha"
SECRET_KEY="auth_nurha"
DB_USER_TABLE="users"
```

### Database Setup
Ensure your PostgreSQL database is running and the credentials match those in your .env file. Create the database and user table as needed.

### Running the Application

1. **Run the FastAPI application:**:
   ```bash
   uvicorn main:app --reload
    ```
   
2. **Access the API documentation:**
   Open your browser and navigate to http://127.0.0.1:8000/docs to see the interactive API documentation provided by Swagger UI.
   
