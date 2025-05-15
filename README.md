# AutoRia Scraper

## Description

This project is a program for periodic scraping of the AutoRia platform. The program collects data about car listings from all pages starting from a hardcoded URL, visits each car’s detail page, and extracts detailed information such as title, price, odometer, VIN, contact info, and images. The data is stored in a PostgreSQL database. The program also creates daily database dumps and stores them in the `dumps` folder.

---

## Functionality

- **Daily Scraping**: The program runs once a day at 12:00 PM Kyiv time, scrapes all pages starting from a given URL, and visits each car detail page.
- **Detailed Data Collection**: For each listing, the program collects:
  - `url`
  - `title`
  - `price_usd`
  - `odometer` (converted to integer km)
  - `image_url` (main photo)
  - `images_count`
  - `car_number`
  - `car_vin`
  - `datetime_found`
- **No Duplicates**: The scraper avoids inserting duplicate data based on unique constraints such as `url` or `car_vin`.
- **Daily Database Dumps**: The program creates a database dump at 12:00 PM Kyiv time every day and stores it in the `dumps/` directory.
- **Logging**: All program actions are logged using the `loguru` library, with log rotation (1 GB).

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/OleksandrDoronin/test_task_parser.git
```
### 2. Create the .env file
Copy the .env.example file to .env and configure it:
```bash
cp .env.example .env
```

### Configure Environment Variables
- `POSTGRES_HOST`: The hostname of the PostgreSQL database.
- `POSTGRES_PORT`: The port of the PostgreSQL database.
- `POSTGRES_DB`: The name of the PostgreSQL database.
- `POSTGRES_USER`: The username for the PostgreSQL database.
- `POSTGRES_PASSWORD`: The password for the PostgreSQL database.

---

## Installing Docker and Docker Compose

Before you can use Docker and Docker Compose, you need to install them on your system.

### Installing Docker on Linux

1. **Download and Install Docker:**

   Run the following commands to automatically install Docker:

   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

2. **Install Docker Compose:**

    Download the latest version of Docker Compose:
    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)"  -o /usr/local/bin/docker-compose
    sudo mv /usr/local/bin/docker-compose /usr/bin/docker-compose
    sudo chmod +x /usr/bin/docker-compose
    docker compose version
    ```

### Installing Docker on macOS

1. **Install Docker:**

    To install Docker on macOS, use Homebrew:
    ```bash
    brew install docker
    ```

2. **Install Docker Compose:**

    Install Docker Compose via Homebrew as well:
    ```bash
    brew install docker-compose
    ```

## Using Docker and Docker Compose

Docker Compose is used to simplify the setup of development and production environments.

### 1. Build and Run the Containers

Use the following commands to start the application in a containerized environment:

```bash
docker-compose up --build
```

If you want to run the containers in the background, you can add the -d flag:

```bash
docker-compose up --build -d
```

### 2. Stop the Containers
To stop the running containers:
```bash
docker-compose stop
```
---
This `README.md` will help other developers understand how to set up, run, and work with your project.

