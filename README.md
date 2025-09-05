# CineScope API

A robust, RESTful backend API for the CineScope movie discovery application. This API serves as a secure proxy and data processor for the TMDB (The Movie Database) API, providing clean, modeled, and cached data for a modern frontend.

---

## Features

- **Secure Proxy:** Protects the TMDB API key by handling all external requests on the server-side.
- **Data Modeling:** Aggregates data from multiple TMDB endpoints and provides clean, structured JSON responses.
- **Performance:** Implements caching to reduce latency and avoid API rate limits.
- **Smart Search:** Provides a search endpoint for finding movies.
- **Automated Testing:** Includes a suite of `pytest` tests to ensure reliability.

---

## Tech Stack

- **Framework:** Flask
- **External API:** TMDB (The Movie Database)
- **Caching:** Flask-Caching
- **Testing:** pytest
- **Deployment:** Gunicorn

---

## Setup & Installation

Follow these steps to run the project locally.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/cinescope-api.git](https://github.com/your-username/cinescope-api.git)
    cd cinescope-api
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For PowerShell on Windows
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the project root and add your TMDB API Read Access Token.
    ```env
    TMDB_API_KEY="YOUR_API_KEY_HERE"
    ```

5.  **Run the application:**
    ```bash
    flask run
    ```
    The API will be available at `http://127.0.0.1:5000`.

---

## API Endpoint Documentation

All endpoints are prefixed with `/api/v1`.

| Method | Endpoint                    | Description                                         |
| :----- | :-------------------------- | :-------------------------------------------------- |
| `GET`  | `/movies/popular`           | Returns a list of popular movies.                   |
| `GET`  | `/movies/top-rated`         | Returns a list of top-rated movies.                 |
| `GET`  | `/movies/upcoming`          | Returns a list of upcoming movies.                  |
| `GET`  | `/movies/<int:movie_id>`    | Returns detailed information for a single movie.    |
| `GET`  | `/movies/search?title=...`  | Searches for movies by title.                       |

---

## Running Tests

To ensure the application is working correctly, run the automated test suite:

```bash
pytest
```