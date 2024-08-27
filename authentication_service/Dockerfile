# Use the official Python slim image
FROM python:3.8-slim

# Set the working directory inside the container to /authentication_service
WORKDIR /authentication_service

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code to the container
COPY . .

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/authentication_service

# Run the FastAPI application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
