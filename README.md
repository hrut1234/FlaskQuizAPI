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
    ```bash
    Once the application is running, you can access the API endpoints using the following URLs:
        Create a Quiz: POST http://localhost:5000/quiz/
        Get a Quiz: GET http://localhost:5000/quiz/<quiz_id>/
        Submit an Answer: POST http://localhost:5000/quiz/<quiz_id>/question/<question_id>/answer/
        Get Results: GET http://localhost:5000/quiz/<quiz_id>/result/<user_id>/
        List All Quizzes: GET http://localhost:5000/quizzes/
    ```

4. **API Endpoints:**
    1. Create a Quiz
        Endpoint: POST /quiz/
        Description: Creates a new quiz.
        Request Body:
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
        Endpoint: GET /quiz/<string:quiz_id>/
        Description: Retrieves a quiz by its ID.
        URL Parameters:
            quiz_id (string): The ID of the quiz.
    3. Submit an Answer
        Endpoint: POST /quiz/<string:quiz_id>/question/<string:question_id>/answer/
        Description: Submits an answer for a specific question in a quiz.
        URL Parameters:
            quiz_id (string): The ID of the quiz.
            question_id (string): The ID of the question.
        Request Body:
        ```bash
        {
        "selected_option": "3"
        }
        ```
    4. Get Results
        Endpoint: GET /quiz/<string:quiz_id>/result/<string:user_id>/
        Description: Retrieves the results for a specific user for a given quiz.
        URL Parameters:
            quiz_id (string): The ID of the quiz.
            user_id (string): The ID of the user.
    5. List All Quizzes
        Endpoint: GET /quizzes/
        Description: Retrieves a list of all available quizzes.

4. **API Limitations:**
    Data Persistence: Currently, the API does not include a persistent storage solution. Data will be lost when the application is restarted or stopped.
    Input Validation: Basic input validation is implemented. However, additional validation and error handling may be required to ensure data integrity and security.
    Authentication & Authorization: The API does not include authentication or authorization mechanisms. This should be considered for protecting sensitive endpoints and managing user access.