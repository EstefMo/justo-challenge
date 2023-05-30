# Use an official Python runtime as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN apt-get update && apt-get install -y libpq-dev
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY spyagency /code

# Introduce a delay of 10 seconds (adjust as needed)
RUN sleep 20

# Expose the port the Django server will run on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
