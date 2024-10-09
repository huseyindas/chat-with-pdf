# CHAT WITH PDF

## Project Overview

This project is a FastAPI application integrated with Ollama, PGVectorDB, and Redis, designed to interact with PDF documents and provide AI-generated responses. It includes several endpoints for uploading PDFs and querying information from them, as well as health check mechanisms and rate limiting to ensure stability and performance.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed on your machine.
- A GPU (optional) for enhanced performance.

### Environment Configuration

1. **Clone the repository:**
    ```bash
    git clone https://github.com/huseyindas/chat-with-pdf.git
    cd chat-with-pdf
   ```

2. Copy the example environment file:
    - Rename .env.example to .env:
    ```bash
    cp .env.example .env
    ```
    Edit .env as necessary to configure your environment settings.

## Starting the Application
To start the FastAPI application with Docker Compose, you can use the provided start.sh script:

1. Make the script executable:
    ```bash
    chmod +x start.sh
    ````
2. Run the application:
   - To build the containers:
    ```bash
    ./start.sh build
    ```
   - To run without rebuilding:
    ```bash
    ./start.sh
    ```
    The script will check for GPU support and run the appropriate Docker Compose configuration (docker-compose.yml for CPU or docker-compose.gpu.yml for GPU).

## API Endpoints

#### 1. Chat with PDF
    * Request Method: POST
    * Endpoint: /v1/chat/{pdf_id}
    * Description: Interact with a specific PDF.

    * Input:
        {
        "message": "What is the main topic of this PDF?"
        }

    * Output:
        {
        "response": "The main topic of this PDF is <topic>."
        }


#### 2. Upload PDF
    * Request Method: POST
    * Endpoint: /v1/pdf
    * Description: Upload and register a PDF.
    * Input: Multipart form data containing the PDF file.

    * Example:
        curl -X POST "http://localhost:8000/v1/pdf" \
        -F "file=@/path/to/your/pdf/file.pdf"

    * Output:
        {
        "pdf_id": "unique_pdf_identifier"
        }

#### 3. Health Check
    * Request Method: GET
    * Endpoint: /v1/health
    * Description: Check the health status of the application.

<br>

## Rate Limiting

Upload PDF and chat endpoints are rate-limited to 3 requests per minute.
Health check endpoint is limited to 1 request per second.

## Middleware
The application includes several middleware components:

**CustomTimeoutHandlingMiddleware**: Handles a 120-second timeout.
**CustomErrorHandlingMiddleware**: Manages exceptions within the application.
**CustomHealthCheckMiddleware**: Ensures Ollama, PGVector, and Redis are running before processing requests.

## Documentation
Access the API documentation at **/docs** (Swagger UI).

- AI and LangChain codes can be found in src/ai.
- Endpoint implementations are located in src/pdf and src/chat.
- Core operations, including middleware, rate limiting, logging, Redis, and database files, are in src/core.


## Testing Procedures

### Running Tests

- To run the test suite, ensure that Ollama, PGVector, and Redis are running in Docker or on your system.

- Check the environment file: Ensure that .env.pytest has the necessary configurations.

- The run_tests.sh script exports the environment variables from .env.pytest and runs the test suite using pytest.

**Run the tests:**

```bash
sh run_tests.sh
```

## Conclusion

This FastAPI application provides a robust solution for interacting with PDF documents using AI technologies. Follow the setup instructions and utilize the API endpoints to leverage its capabilities effectively.
