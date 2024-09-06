# Quiz API

Welcome to the Quiz API! This Flask-based API allows you to create quizzes, retrieve quiz details, submit answers, and view quiz results. The application is containerized using Docker Compose for streamlined setup and deployment.

## Getting Started

### Prerequisites

Ensure you have the following installed on your machine:

- Docker
- Docker Compose

### Running the Application

1. **Clone the repository:**

   ```bash
   git clone https://github.com/hrut1234/FlaskQuizAPI
   ```
   

2. **Build and start the Docker containers:**
    ```bash
    cd FlaskQuizAPI
    docker-compose up --build -d
    ```

3. **Accessing API Endpoints:**
    Once the application is running, you can access the API endpoints using the following URLs:
    
    1. Create a Quiz: POST http://localhost:5000/quiz/
    2. Get a Quiz: GET http://localhost:5000/quiz/<quiz_id>/
    3. Submit an Answer: POST http://localhost:5000/quiz/<quiz_id>/question/<question_id>/answer/
    4. Get Results: GET http://localhost:5000/quiz/<quiz_id>/result/<user_id>/
    5. List All Quizzes: GET http://localhost:5000/quizzes/
  

4. **API Endpoints:**
    1. Create a Quiz
        1. Endpoint: POST /quiz/
        2. Description: Creates a new quiz.
        3. Request Body:
        ```bash
            {
            "title": "Quiz Title",
            "description": "Quiz Description",
            "questions": [
                {
                "question": "What is the capital of France?",
                "options": ["Paris", "London", "Berlin", "Delhi"],
                "correct_option": "3"
                }
            ]
            }
        ```
    2. Get a Quiz
        1. Endpoint: GET /quiz/<string:quiz_id>/
        2. Description: Retrieves a quiz by its ID.
        3. URL Parameters:
            1. quiz_id (string): The ID of the quiz.
    3. Submit an Answer
        1. Endpoint: POST /quiz/<string:quiz_id>/question/<string:question_id>/answer/
        2. Description: Submits an answer for a specific question in a quiz.
        3. URL Parameters:
            1. quiz_id (string): The ID of the quiz.
            2. question_id (string): The ID of the question.
        4. Request Body:
        ```bash
        {
        "selected_option": "3"
        }
        ```
    4. Get Results
        1. Endpoint: GET /quiz/<string:quiz_id>/result/<string:user_id>/
        2. Description: Retrieves the results for a specific user for a given quiz.
        3. URL Parameters:
            1. quiz_id (string): The ID of the quiz.
            2. user_id (string): The ID of the user.
    5. List All Quizzes
        1. Endpoint: GET /quizzes/
        2. Description: Retrieves a list of all available quizzes.

4. **API Limitations:**
    1. Data Persistence: Currently, the API does not include a persistent storage solution. Data will be lost when the application is restarted or stopped.
    2. Input Validation: Basic input validation is implemented. However, additional validation and error handling may be required to ensure data integrity and security.
    3. Authentication & Authorization: The API does not include authentication or authorization mechanisms. This should be considered for protecting sensitive endpoints and managing user access.

5. **API Issues:**
    1. User's score keeps getting increaed for multiple post requests for the same question.
    2. Use a unique identifier for each user's answer to a specific question. Store this in a database to track whether an answer has already been submitted.