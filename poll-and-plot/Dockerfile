# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY poll_and_plot.py /app

RUN mkdir /app/output

# Install any needed packages specified in requirements.txt
RUN pip install requests matplotlib

# Make the port 80 available to the world outside this container
EXPOSE 80

# Set the entry point to the Python script
ENTRYPOINT ["python", "poll_and_plot.py"]
