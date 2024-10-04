# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies first
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Set the environment variable for the port
ENV PORT=5555

# Expose the port
EXPOSE 5555

# Command to run your application
CMD ["python", "appData.py"]
