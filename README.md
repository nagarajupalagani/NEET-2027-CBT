# NEET 2027 Physics CBT Portal — Test 01

## What it does
One student URL for a 50-question, 60-minute NEET-style Physics test and a password-protected teacher dashboard. Student submissions are scored on the server, so the answer key is not exposed in the browser code.

Topics: Units & Measurements (15), Motion in a Straight Line (20), Motion in a Plane (15).
Marking: +4 correct, -1 wrong, 0 unattempted. Dashboard includes ranking, scores, correct/wrong/unattempted, time taken, and CSV export.

## Publish
Upload the project to a Python-capable host. Install:
`pip install -r requirements.txt`

Set environment variables:
- `SECRET_KEY`: long random secret
- `TEACHER_PASSWORD_HASH`: Werkzeug hash of your chosen teacher password
- `DATABASE_PATH`: optional persistent path for SQLite

Generate a password hash:
`python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('YOUR_PASSWORD'))"`

Start command on Gunicorn-capable hosting:
`gunicorn app:app`

Student page: `/`
Teacher login: `/teacher`

IMPORTANT: Use persistent storage for the SQLite database. If the host has an ephemeral filesystem, results can disappear after restarts; use managed PostgreSQL for production.
