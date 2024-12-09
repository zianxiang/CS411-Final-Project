# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install SQLite3 if needed (if your app uses SQLite)
RUN apt-get update && apt-get install -y sqlite3

# Copy SQL scripts if needed
COPY ./sql/create_db.sh /app/sql/create_db.sh
COPY ./sql/create_meal_table.sql /app/sql/create_meal_table.sql

# Make the shell script executable
RUN chmod +x /app/sql/create_db.sh

# Set a volume for the database if needed
VOLUME ["/app/db"]

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the application entrypoint (adjust according to your app's entry point)
CMD ["/app/entrypoint.sh"]

