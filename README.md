# School Management System

A web-based School Management System developed using Python and Django. This project is designed for local development and administration through Django's built-in admin interface.

## Project Overview

The School Management System provides a foundation for managing school-related data using Django and SQLite. The application runs locally on your computer through Django's development server.

## Technologies Used

- Python
- Django
- SQLite
- Django Administration
- Git and GitHub
- Visual Studio Code

## Project Structure

```text
school_management/
├── manage.py
├── requirements.txt
├── school/
├── school_project/
├── README.md
└── .gitignore
```

## Requirements

- Python 3
- pip
- Visual Studio Code (recommended)

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Chyaitanya12/school_management.git
cd school_management
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create an administrator account

```bash
python manage.py createsuperuser
```

Enter your username, email address, and password when prompted.

### 7. Start the Django development server

```bash
python manage.py runserver
```

### 8. Open Django Administration

Open the following URL in your browser:

[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

Log in using the administrator credentials created in Step 6.

## Database

This project uses SQLite as its configured database. Django manages database tables through migrations.

## Running the Project

Whenever you want to run the project locally:

1. Open the project folder in VS Code.
2. Activate the virtual environment.
3. Run `python manage.py runserver`.
4. Open [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) in your browser.

Stop the development server by pressing `Control + C` in the terminal.

## Project Purpose

This project helps develop practical experience with Python, Django, database management, and web application administration.

## Author

**Chyaitanya**

GitHub Repository: [https://github.com/Chyaitanya12/school_management](https://github.com/Chyaitanya12/school_management)

## License

This project is intended for educational and learning purposes.
