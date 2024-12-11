# CS411-Final-Project
Secure Password Storage
○ Database:
■ Create a SQLite table to store usernames, salts, and hashed passwords.
You can implement this using either SQLAlchemy directly or raw SQLite
commands. Using SQLAlchemy is recommended for ease of code re-use.
○ Routes:
■ /login: Checks the provided password against the stored hash. This
route doesn't need to handle actual user sessions.
■ /create-account: Allows new users to register by providing a
username and password.
■ /update-password: Enables users to change their password.