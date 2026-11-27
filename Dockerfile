FROM python:3.11-slim

# Work from the project root inside the container
WORKDIR /app

# Install the requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the files the API needs
COPY api/ /app/api/
COPY data/ /app/data/

# Start the API from the project root
CMD ["python", "api/main.py"]