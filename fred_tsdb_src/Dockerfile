# Uses the "getting started" example as a base:
# https://docs.docker.com/get-started/part2/#define-a-container-with-dockerfile

# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Make all necessary ports visible
EXPOSE 8000

USER root

# Install prometheus_client and quandl
RUN pip install --trusted-host pypi.python.org -r /app/requirements.txt

# Define environment variable
ENV NAME World

CMD ["python", "initTSDB.py"]