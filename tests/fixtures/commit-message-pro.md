Change: the session cookie was readable by JavaScript. Added HttpOnly and
SameSite=Lax, and moved the CSRF token to its own cookie so the form still works.
Touched auth/session.py and templates/base.html. The repo uses conventional
commits.
