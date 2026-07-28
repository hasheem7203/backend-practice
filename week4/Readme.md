# FlyRank Auth API — Login & Protect

A small FastAPI service that uses **Supabase Auth** as its identity provider:
sign up, log in, log out, and a reusable guard that protects specific routes
by verifying a JWT on every request.

## What this is

This project does **not** hash passwords or issue tokens itself. Supabase
does that. The server's job is: forward credentials to Supabase, and verify
the JWT Supabase hands back before opening a protected route.

## Setup

1. Clone this repo and `cd` into it.
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your own Supabase project values
   (Project Settings → API in your Supabase dashboard):
   ```
   SUPABASE_URL=your_project_url_here
   SUPABASE_KEY=your_anon_key_here
   PORT=8000
   ```
   Use the **anon** key — never the `service_role` key here.
4. In your Supabase dashboard, go to Authentication → Sign In / Providers →
   Email, and turn **off** "Confirm email" (so a fresh signup can log in
   immediately for testing).

## Run

```bash
uvicorn main:app --reload --port 8000
```

Then open **http://localhost:8000/docs** for interactive Swagger UI.

## Endpoint reference

| Method | Route                  | Purpose                    | Auth required          |
|--------|-------------------------|-----------------------------|--------------------------|
| POST   | `/auth/signup`           | Create a new user account   | None                     |
| POST   | `/auth/login`            | Authenticate & return a JWT | None                     |
| POST   | `/auth/logout`           | End the user's session      | `Authorization: Bearer <token>` |
| GET    | `/protected/profile`     | Read private profile data   | `Authorization: Bearer <token>` |
| GET    | `/protected/dashboard`   | Second protected route (proves the guard is reusable) | `Authorization: Bearer <token>` |
| GET    | `/public/info`           | Read public, open data      | None                     |

## Status codes

| Code | When |
|------|------|
| 201  | Signup succeeds |
| 200  | Login succeeds / protected data read |
| 204  | Logout succeeds |
| 400  | Missing email or password |
| 401  | Missing, malformed, invalid, or expired token — or bad login credentials |

## Testing it

```bash
# Sign up
curl -i -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Log in (grab the access_token from the response)
curl -i -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Call a protected route
curl -i http://localhost:8000/protected/profile \
  -H "Authorization: Bearer <PASTE_ACCESS_TOKEN_HERE>"

# No token -> 401
curl -i http://localhost:8000/protected/profile
```

Or skip curl entirely: open `/docs`, click **Authorize**, paste your access
token, and use **Try it out** on any protected route.

