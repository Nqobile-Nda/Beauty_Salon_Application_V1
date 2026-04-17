# Carol's Beauty Lounge

Carol's Beauty Lounge is a Flask web application for managing a small beauty service business. It provides an admin dashboard for managing services, booking requests, and appointments, alongside a user-facing experience for browsing services and submitting bookings.

## Overview

This project was built as a practical salon management application and learning project. It currently uses Flask, Jinja templates, JavaScript, and JSON file storage, with future plans to move to SQLite as the project grows.

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
- JSON for current data storage

## Project Structure

```text
CBL/
|-- app.py
|-- data_manager.py
|-- requirements.txt
|-- .gitignore
|-- .env
|-- catalog.json
|-- booking_requests.json
|-- appointments.json
|-- static/
|   |-- style.css
|   |-- script.js
|   `-- images/
`-- templates/
    |-- admin/
    `-- user/
```

## Data Storage

The app currently stores data in:

- `catalog.json`
- `booking_requests.json`
- `appointments.json`

This setup keeps the project simple for local development and learning. A database-backed version can be introduced later.

## Local Setup

1. Create and activate a virtual environment.
2. Install the project dependencies:

```powershell
pip install -r requirements.txt
```

3. Add a `.env` file in the project root:

```env
SECRET_KEY="your-secret-key"
```

4. Start the application:

```powershell
python app.py
```

5. Open it in the browser:

```text
http://127.0.0.1:5000
```

## Default Admin Credentials

Current admin login details:

- Username: `user`
- Password: `password`

These credentials are hardcoded for development and should be replaced before production use.

## Current Limitations

- JSON storage is not ideal for multi-user or production usage
- Admin credentials are still hardcoded
- File upload sanitization still needs improvement
- Some flows are still being refined for deployment readiness

## Roadmap

- Move persistence from JSON files to SQLite
- Improve validation and error handling
- Add safer authentication and credential management
- Improve deployment readiness

## Summary

Carol's Beauty Lounge is a beginner-friendly full-stack Flask project that combines salon service management with a customer booking flow. It is designed to be simple enough to learn from while still covering real application features such as authentication, CRUD operations, image uploads, and booking management.
