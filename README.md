# FastAPI Todos Application

A complete CRUD (Create, Read, Update, Delete) application for managing a "to-do" list, built with FastAPI and deployed on Render. The application features user authentication with JWT, password hashing, and a relational database managed with SQLAlchemy and Alembic.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/downloads/release/python-311/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103-green.svg)](https://fastapi.tiangolo.com/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-cyan.svg)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Live Demo

The application is deployed and accessible on Render. You can interact with the live API documentation here:

**[https://todosapp-5ubg.onrender.com/docs](https://todosapp-5ubg.onrender.com/docs)**

---

## Key Features

-   **User Authentication**: Secure user registration and login using JWT access tokens.
-   **Password Hashing**: Passwords are never stored in plaintext, using `bcrypt` for hashing.
-   **Full CRUD Functionality**: Create, read, update, and delete to-do items.
-   **Database Integration**: Uses SQLAlchemy ORM to interact with a PostgreSQL database.
-   **Database Migrations**: Alembic is configured to handle database schema changes.
-   **Dependency Injection**: Leverages FastAPI's dependency injection system for database sessions and user authentication.
-   **Interactive API Docs**: Automatic, interactive API documentation provided by FastAPI (via Swagger UI and ReDoc).

---

## Technology Stack

-   **Backend**: Python, FastAPI
-   **Database**: PostgreSQL
-   **ORM**: SQLAlchemy
-   **Data Validation**: Pydantic
-   **Authentication**: python-jose, passlib[bcrypt]
-   **Database Migrations**: Alembic
-   **Deployment**: Render

---

## Project Structure

```
.
├── alembic/              # Alembic migration scripts
├── app/                  # Main application source code
│   ├── __init__.py
│   ├── database.py       # Database session management
│   ├── main.py           # FastAPI app instance and root endpoints
│   ├── models.py         # SQLAlchemy ORM models
│   ├── routers/          # API endpoint routers
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   └── auth.py
│   └── ...
├── alembic.ini           # Alembic configuration
├── requirements.txt      # Python dependencies
└── README.md
```

---

## Local Setup and Installation

Follow these steps to run the project on your local machine.

### 1. Prerequisites

-   Python 3.9+
-   A running PostgreSQL database instance.

### 2. Clone the Repository

```bash
git clone https://github.com/Mann10/FastAPI.git
cd FastAPI
```

### 3. Create a Virtual Environment

It is highly recommended to use a virtual environment.

```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a file named `.env` in the root of the project and add your PostgreSQL database URL.

```env
# .env
DATABASE_URL=postgresql://user:password@host:port/database_name
```

The application reads this URL to connect to the database.

### 6. Run Database Migrations

Apply the database schema using Alembic. This will create the `users` and `todos` tables.

```bash
alembic upgrade head
```

### 7. Run the Application

Start the local development server using Uvicorn.

```bash
uvicorn app.main:app --reload
```

The application will be running at **http://127.0.0.1:8000**.

---

## API Documentation

Once the server is running, you can access the interactive API documentation at:

-   **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
-   
---

## Deployment on Render

This application is configured for easy deployment on Render.

1.  **Fork this repository** to your GitHub account.
2.  **Create a "Web Service"** on Render and connect it to your forked repository.
3.  **Create a PostgreSQL Database** on Render.
4.  **Set the Environment Variable**:
    -   `Key`: `DATABASE_URL`
    -   `Value`: The "Internal Connection String" from your Render PostgreSQL instance.
5.  Render will automatically detect the `Procfile` and use it as the **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

Render will install the dependencies from `requirements.txt` and start the server.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.
