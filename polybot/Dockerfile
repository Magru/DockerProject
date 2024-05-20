# Use the official Python image as the base image
FROM python:3.9-slim as build

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file into the container
#COPY .env .

# Load environment variables from the .env file
#ENV $(cat .env | xargs)

# Copy the rest of the application code into the container
COPY . .

# Expose the port that the Flask app will run on (replace 5000 with the appropriate port if needed)
EXPOSE 5000

# Set the entry point to run the Flask app
CMD ["python", "app.py"]