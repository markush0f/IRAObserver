# Admin bootstrap flow

This document describes the one-time admin bootstrap flow used when the
application has no administrator user.

## Goal

Prevent access to all application endpoints until an admin exists, while
allowing a minimal set of endpoints to create the first admin.

## API behavior

### Global guard

A global dependency blocks all requests when there is no admin user. Allowed
paths during bootstrap are:

- `GET /auth/bootstrap-status`
- `POST /auth/bootstrap`
- `GET /health`

All other endpoints return:

- `403 Forbidden`
- body: `{ "detail": "admin bootstrap required" }`

### Endpoints

- `GET /auth/bootstrap-status`
  - Response: `{ "needs_bootstrap": true | false }`
  - Used by the frontend to decide whether to show the bootstrap UI.

- `POST /auth/bootstrap`
  - Creates the first admin user.
  - Allowed only if no admin exists.
  - Response codes:
    - `201 Created` with the created admin payload.
    - `409 Conflict` if an admin already exists.

- `POST /auth/register`
  - Admin registration is blocked here.
  - If `role=admin`, returns `403 Forbidden`.

## Frontend flow

1. On first load, call `GET /auth/bootstrap-status`.
2. If `needs_bootstrap` is `true`, show a “Create admin” form.
3. Submit the form to `POST /auth/bootstrap`.
4. On `201`, redirect to the normal login screen.
5. On `409`, redirect to the normal login screen (admin already exists).

## Notes

- The bootstrap endpoint ignores the incoming role and always creates the
  user with `role="admin"`.
- If you want to allow `/docs` or `/openapi.json` during bootstrap, add them
  to the allowlist in `app/api/deps.py`.
