# Backend — Task Tracker Lite

## Quick start (local, without Docker)
1. Create virtualenv:
   python -m venv .venv
   .\.venv\Scripts\activate

2. Install:
   pip install -r requirements.txt

3. Copy .env.example to .env and edit values.

4. Initialize migrations (ensure PostgreSQL running and DATABASE_URL correct):
   flask db init
   flask db migrate -m "initial"
   flask db upgrade

5. Run:
   flask run --host=0.0.0.0

## Notes about JWT + Cookies
- Login endpoint sets a HttpOnly cookie with the access token.
- Frontend must send requests with credentials (fetch/axios with `withCredentials: true`).
- Logout clears cookie via unset_jwt_cookies.
