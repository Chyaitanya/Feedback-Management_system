# Overall Feedback System

Overall Feedback System is a Django feedback portal with **separate student and admin logins**, private student dashboards, an admin management dashboard, and a bright, modern responsive interface.

## What was added

- Separate **Student Login**, **Student Registration**, and **Admin Login** pages.
- Student accounts are connected to an existing Student UID. One UID can have only one login account.
- Students can view their own dashboard and submissions. Their Student UID is attached automatically when they submit feedback.
- Students cannot view other students' feedback or the admin dashboard.
- Admin/staff users can view the full dashboard, faculty list, and feedback responses, and manage records through Django Admin.
- A colorful responsive visual refresh for the portal, login pages, and dashboards.

## Run on macOS (VS Code Terminal)

Open the `school_feedback_system` folder in VS Code. Open **Terminal → New Terminal**, then run:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open the site at http://127.0.0.1:8000/.

## First-time setup

1. Open **Admin Login** at http://127.0.0.1:8000/admin-login/ and sign in with the username and password created by `createsuperuser`.
2. In the admin dashboard, choose **Manage campus data**, or open http://127.0.0.1:8000/admin/.
3. Add Student records with their Student UID, class/standard, and subject. The UID is the student's login ID. You can also run the sample-data command below.
4. Add Faculty records and at least one active Feedback Form.
5. Students open http://127.0.0.1:8000/student/register/, enter their pre-registered Student UID, college email, and a password, then log in at http://127.0.0.1:8000/student/login/.
6. Students submit feedback from their own dashboard. Their UID is assigned automatically and cannot be changed in the feedback form.

## Sample data for quick demonstration

After running migrations, use:

```bash
python manage.py seed_demo
```

This creates sample student, faculty, and active feedback-form records matching the included schema reference:

| Student UID | Class | Subject |
|---|---|---|
| S001 | FY B.Tech | Chemical Engineering |
| S002 | FY B.Tech | Information Technology |
| S003 | SY B.Tech | Chemical Engineering |
| SDEMO | Demo data | Synthetic examples only |

It also creates three sample faculty records (`F001`–`F003`) and two active feedback forms (`FF001`–`FF002`). Students can then register with S001, S002, or S003. Each student chooses their own password during registration.

### Try the feedback demo

1. Open `/student/register/` and create an account using S001, S002, or S003. SDEMO is reserved for synthetic sample responses and has no login account. There is intentionally no shared demo password; each student chooses their own password.
2. Sign in, choose any faculty member and an active feedback form, then rate the overall experience, teaching clarity, communication, and punctuality from 1 to 5.
3. Submit the form. A student can submit once for each faculty member and feedback form; the same combination cannot be submitted twice, while a different faculty member or form can be reviewed separately.
4. The admin Responses page includes fictional sample ratings for SDEMO across the sample faculty and forms. Running `python manage.py seed_demo` again is safe and does not duplicate those examples.

Feedback submissions are unique per student, faculty member, and feedback form. Admins can compare overall, teaching-clarity, communication, and punctuality ratings on the Responses page.

## Deploy to Render

The repository includes a Render Blueprint at [`../render.yaml`](../render.yaml). To deploy:

1. Push the repository to GitHub and sign in to [Render](https://render.com/).
2. For the existing web service, open **Settings** and set **Root Directory** to `feedback_system`, **Build Command** to `pip install -r requirements.txt && python manage.py collectstatic --no-input`, and **Start Command** to `python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`. The failed `gunicorn app:app` command points to the wrong application.
3. Set `PYTHON_VERSION` to `3.12.8` in the service's **Environment** settings. The root-level Blueprint specifies this version as well.
4. To create resources from scratch instead, choose **New → Blueprint**, select `Chyaitanya/school_management`, and review `render.yaml` at the repository root.
5. Review Render's current pricing before creating the PostgreSQL database. The Blueprint uses a persistent PostgreSQL plan; the web service uses the free plan and may sleep when idle.
6. After the first deploy, open the web service's **Shell** and create an admin login with `python manage.py createsuperuser`.
7. Add SMTP credentials in the service's **Environment** settings to enable password reset emails: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, and `DEFAULT_FROM_EMAIL`. Use an email provider's SMTP credentials, not your personal email password.
8. Add students, faculty, and feedback forms from the admin interface. The local SQLite database is not uploaded or copied; run `python manage.py seed_demo` from the Render shell only if you want fictional sample records.

The Blueprint configures a generated `SECRET_KEY`, PostgreSQL, HTTPS-aware security settings, static assets, and database migrations. Keep `DEBUG` disabled in production. Do not commit credentials or a local database.

### Environment variables

Render supplies `DATABASE_URL` and `RENDER_EXTERNAL_HOSTNAME`. The Blueprint generates `SECRET_KEY` and disables `DEBUG`. Configure the SMTP variables listed above in Render to deliver password reset emails. Locally, SQLite and console email remain the defaults.

## Windows PowerShell

```powershell
py -m venv venv
venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

## Important notes

- **Admin account:** created securely by you with `python manage.py createsuperuser`. There is no hard-coded admin password.
- **Student account:** students register only after an admin has added their UID to the Student table. The UID is the username for student login.
- **Existing database:** if you already have a database from the previous version, keep it and run `python manage.py migrate` to add the student-account table.
- SQLite is used by default for local development; the Render Blueprint configures PostgreSQL for deployment.
- The Render Blueprint disables debug mode, generates a secret key, and configures HTTPS-aware settings. Keep production credentials in Render environment variables, not in source control.
- Use sample data for public demos rather than real student personal information.
