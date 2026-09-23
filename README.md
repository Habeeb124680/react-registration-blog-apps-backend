# Blog API (Django + Django REST Framework)

## Run it locally

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API runs at http://127.0.0.1:8000
Django admin (to browse your data): http://127.0.0.1:8000/admin (run `python manage.py createsuperuser` first)

No database setup needed locally — it uses a SQLite file (`db.sqlite3`) automatically.

## Endpoints

| Method | Path              | Auth required | What it does                          |
|--------|-------------------|----------------|----------------------------------------|
| POST   | /auth/register     | no             | Create an account, returns a token     |
| POST   | /auth/login        | no             | Log in, returns a token                |
| GET    | /auth/me           | yes            | Get the logged-in user's info          |
| GET    | /posts             | optional       | List all posts (feed)                  |
| POST   | /posts             | yes            | Create a post                          |
| POST   | /posts/{id}/like    | yes            | Like/unlike a post (toggles)           |
| DELETE | /posts/{id}         | yes            | Delete a post (only your own)          |

Auth uses JWT — send `Authorization: Bearer <access_token>` on protected requests.

## Deploy to Render

1. Push this `backend` folder to a GitHub repo (or a `backend/` subfolder of your existing repo).
2. On Render: **New +** → **Web Service** → connect your GitHub repo.
3. Set:
   - **Root Directory**: `backend` (if it's a subfolder)
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn config.wsgi`
4. On Render: **New +** → **PostgreSQL** → create a free database.
5. Copy its **Internal Database URL**, and add it to your web service's
   Environment tab as `DATABASE_URL`.
6. Also add environment variables:
   - `SECRET_KEY` — any random string
   - `DEBUG` — `False`
   - `ALLOWED_HOSTS` — your Render URL, e.g. `your-api.onrender.com`
   - `CORS_ORIGINS` — your deployed React app's URL, e.g. `https://your-app.vercel.app`
7. Deploy. Render gives you a public URL like `https://your-api.onrender.com`.