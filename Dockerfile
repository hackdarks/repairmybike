ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy Django project to container
COPY . /app/

# Expose Django port
EXPOSE 8000

# Run Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
