# DjangoWeatherReminder

A web application using DRF is a service of weather notifications.

This application has the following features:

- For getting actual weather data, DjangoWeatherReminder uses OpenWeather api service;

- After registration/authorization clients receive JWT token for further access to the application;

- Users can subscribe to weather notifications, choose cities and period of notification(1, 3, 6 or 12 hours) via rest api;

-  Users can add/update/delete their subscriptions, update period of notification/cities and cancel the subscription via rest api;

- Clients get notifications every period specified in the subscription via email;

The application has been packaged into a Docker container.

## Requirements

- Python 3.9+
- Django 4.2+
- Docker

## Installing

1. [Install Docker](https://www.docker.com/)
2. Clone the repository:
    ```bash
    git clone https://github.com/AlexShv/DjangoWeatherReminder.git

    ```
3. Activate your virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install requirements:
    ```bash
    pip3 install -r requirements.txt
    ```

## Usage

Use docker containers to run the application:
```bash
docker-compose up
```
