# chat-with-pdf
This repository contains a FastAPI implementation designed to allow users to interact with PDF files via chat APIs.

### Todos: 
- Implement error handling for API rate limits, timeouts, and other
potential issues.
- Consider implementing caching mechanisms to improve response times
for frequently asked questions. (Optional)

- Implement detailed logging for all critical operations, including
PDF processing, API calls, and state management.

- Implement different log levels (DEBUG, INFO, WARNING, ERROR) for
granular control over log output. (Optional)

- Unit tests for individual components (e.g., PDF processing, Gemini
API integration, state management).
- Integration tests to verify the entire application flow, including
API endpoints and error handling.

- Develop a comprehensive README.md file including:
    * Project overview
    * Detailed setup instructions, including environment
    * configuration
    * Explanation of API endpoints with request/response examples
    * Testing procedures and instructions for running the test suite



- Problem 1: Is using the Gemini 1.5 Flash that has 1 Million
context size enough or Retrieval-Augmented Generation (RAG) is a
better approach?
- Problem 2: Having 1 Million context size is great but output
tokens are limited to 8196, how would you queries that has more
than 8196 tokens?
- Problem 3: Writing unit tests are great for ensuring the app works
just fine, but how would you evaluate the performance of the Large
Language Model?