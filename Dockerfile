FROM python:3.12-slim-bullseye

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements.txt file into the container
COPY requirements.txt /code/

# Upgrade pip package manager to the latest version
RUN pip install --upgrade pip

# Install Python dependencies listed in the requirements.txt file
RUN pip install -r requirements.txt

# Copy the contents of the current directory (in Docker context) into the container's /app directory
COPY . /code/

# Copy the entrypoint.sh script into the container
COPY entrypoint.sh /entrypoint.sh

# Grant execution permissions to the entrypoint.sh script inside the container
RUN chmod +x /entrypoint.sh

# Set the entry point for the container, running the entrypoint.sh script
ENTRYPOINT ["bash", "/entrypoint.sh"]