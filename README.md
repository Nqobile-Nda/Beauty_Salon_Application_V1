# Carol's Beauty Lounge

Carol's Beauty Lounge is a Flask web application for managing a small beauty service business. It provides an admin dashboard for managing services, booking requests, and appointments, alongside a user-facing experience for browsing services and submitting bookings.

## Overview

This project was built as a practical salon management application and learning project. It currently uses Flask, Jinja templates, JavaScript, and SQLite for persistent storage.

## Features

- Admin login with session-based access control
- Catalog management for salon services
- Image uploads for catalog items
- Customer booking request submission
- Booking request review for admins
- Appointment creation and viewing
- Category-based service browsing for users
- Modal-based item and appointment details

## Admin Experience

The admin side allows staff to:

- Log in to a protected dashboard
- Add, edit, and delete catalog items
- Review booking requests
- Create appointments manually
- View appointment records

## User Experience

The user side allows customers to:

- Browse the salon catalog
- Filter services by category
- View service details in modals
- Submit booking requests

## Tech Stack

- Python
- Flask
- Jinja2
- HTML
- CSS
- JavaScript
- `python-dotenv`
- SQLite

## Project Structure

```text
CBL/
|-- app.py
|-- data_manager.py
|-- requirements.txt
|-- .gitignore
|-- .env
|-- CBL.db
|-- models/
|   |-- catalog.py
|   |-- bookings.py
|   `-- appointments.py
|-- static/
|   |-- style.css
|   |-- script.js
|   `-- images/
`-- templates/
    |-- admin/
    `-- user/
```

## Data Storage

The app currently stores data in SQLite:

- `CBL.db`

The main tables are:

- `catalog`
- `booking_requests`
- `appointments`


## Local Setup

1. Create and activate a virtual environment.
2. Install the project dependencies:

```powershell
pip install -r requirements.txt
```

3. Add a `.env` file in the project root:

```env
SECRET_KEY="your-secret-key"
ADMIN_USERNAME="your-admin-username"
ADMIN_PASSWORD_HASH="your-generated-password-hash"
```

4. Start the application:

```powershell
python app.py
```

5. Open it in the browser:

```text
http://127.0.0.1:5000
```

To generate a password hash for `ADMIN_PASSWORD_HASH`:

```powershell
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your-password'))"
```

## Admin Credentials

Admin login credentials are loaded from environment variables:

- `ADMIN_USERNAME`
- `ADMIN_PASSWORD_HASH`

The application raises an error on startup if these values are missing.

## Current Limitations

- File upload sanitization still needs improvement
- Some flows are still being refined for deployment readiness

## Roadmap

- Improve validation and error handling
- Add safer authentication and credential management
- Improve deployment readiness

## Summary

Carol's Beauty Lounge is a beginner-friendly full-stack Flask project that combines salon service management with a customer booking flow. It is designed to be simple enough to learn from while still covering real application features such as authentication, CRUD operations, image uploads, and booking management.
