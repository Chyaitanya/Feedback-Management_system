# Feedback Management System

A Django-based education repository with a school management application and a separate student-and-faculty feedback portal. The feedback app provides secure student accounts, private dashboards, faculty evaluations, and admin tools for feedback and campus data.
## Project Overview

This repository contains the root school management system and the separate Overall Feedback System in [feedback_system/](./feedback_system/). The feedback app supports student registration and private feedback submissions; administrators manage students, faculty, feedback forms, and responses. See the [feedback system README](./feedback_system/README.md) for setup, demo data, and deployment instructions.
## Technologies Used

- Python and Django
- SQLite for local development
- PostgreSQL for the Render deployment
- Django Administration
- Git and GitHub
- Visual Studio Code

## Project Structure

```text
Feedback-Management_system/
├── manage.py
├── requirements.txt
├── school/
├── school_project/
├── feedback_system/
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
git clone https://github.com/Chyaitanya/Feedback-Management_system.git
cd Feedback-Management_system
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

The root school management application uses SQLite locally. The separate feedback application also uses SQLite locally and is configured for PostgreSQL on Render. Django manages database tables through migrations.

## Running the Project

Whenever you want to run the root school management application locally:

1. Open the repository folder in VS Code.
2. Activate the virtual environment.
3. Run `python manage.py runserver`.
4. Open [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) in your browser.

To run the feedback application, follow its [README](./feedback_system/README.md) from the `feedback_system/` folder. Stop a development server by pressing `Control + C` in the terminal.

## Project Purpose

This project demonstrates practical use of Python, Django, database migrations, school administration, and student/faculty feedback workflows.

## Author

**Chyaitanya**

GitHub Repository: [https://github.com/Chyaitanya/Feedback-Management_system](https://github.com/Chyaitanya/Feedback-Management_system)

## License

This project is intended for educational and learning purposes.

## Student & Faculty Feedback System

The [`feedback_system/`](./feedback_system/) folder contains the Overall Feedback System, a separate Django application for student feedback. It includes student registration and dashboards, faculty feedback forms, and an admin dashboard.

Follow the [feedback system README](./feedback_system/README.md) for its setup instructions, demo data, and feature details. Run it from that folder; it has its own `manage.py`, dependencies, settings, and SQLite database.

The SQLite database and virtual environments are intentionally excluded from Git. Create a local database with `python manage.py migrate`, then optionally load fictional examples with `python manage.py seed_demo`.

To deploy the feedback system on Render, follow the [deployment guide](./feedback_system/README.md#deploy-to-render). The root-level [`render.yaml`](./render.yaml) Blueprint points Render to `feedback_system/`; review the PostgreSQL plan's current price before creating resources, and add SMTP credentials to enable password reset emails.

GitHub hosts this project's source code; it does not run Django applications.
