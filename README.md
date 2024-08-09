# FastAPI Weather Service

A RESTful API built with FastAPI to serve weather data, including minimum, maximum, average temperatures, and humidity for a given city and date. This service fetches weather data from the https://www.weatherapi.com/ API and caches it using an SQLite database to reduce redundant API calls.

## Features

- **Weather Data API**: Fetch minimum, maximum, average temperature, and humidity for a specified city and date.
- **Data Caching**: Weather data is cached in an SQLite database to avoid duplicate API calls.
- **Docker Support**: Containerized application using Docker for easy deployment.
- **CI/CD**: Automated testing and deployment via GitHub Actions.
- **Unit Testing**: Includes unit test using pytest to ensure functionality.

## Setup

### Prerequisites

- Python 3.10 or higher
- Docker (optional, for containerized setup)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Parissai/fastapi-weather-service.git
   cd fastapi-weather-service
   ```

2. **Create a Virtual Environment (Optional but recommended)**
    ```bash
    python -m venv venv
    ```
3. **Activate the Virtual Environment**

    On Windows:
    ```bash
    venv\Scripts\activate
    ```
    On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

4. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration
Before running the service, you'll need to configure your environment. Rename [.env.example](.env.example) file to .env in the project root and add your API key.

### Usage

To start the FastAPI weather service, run the following command:

```bash
uvicorn app.main:app --reload
```

- Host: http://127.0.0.1:8000
Documentation: Access the interactive 
- API documentation at http://127.0.0.1:8000/docs.

### Endpoint

#### Get Historical Weather: `/weather?city={city}&date={date}`
**Description:** 

Retrieve historical weather data for a specified city on a given date.

**Query Parameters:**
- **city (string):** The name of the city you want to get the historical weather for.
- **date (string):** The specific date for which you want to retrieve historical weather, formatted as YYYY-MM-DD.

### Run the Tests
```bash
pytest
```
