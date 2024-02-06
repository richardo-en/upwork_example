# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Install gcc and other build dependencies
RUN apk add --no-cache gcc musl-dev

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# RUN pip install greenlet --no-cache-dir
# RUN pip install Cmake
RUN pip install --no-cache-dir -r requirements.txt

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "upwork_example/app.py"]
