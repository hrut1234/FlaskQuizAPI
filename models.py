import uuid
import hashlib
from pymongo import MongoClient

# Initialize MongoDB client
client = MongoClient("mongodb://mongo:27017/")  # Use the appropriate MongoDB URI
db = client.quiz_db  # Use or create a database named 'quiz_db'

# Define MongoDB collections
quizzes_collection = db.quizzes
questions_collection = db.questions
results_collection = db.results

def hash_question(text, options):
    """
    Generates a hash for a question based on its text and options.
    
    Args:
    - text (str): The text of the question.
    - options (list): A list of answer options.

    Returns:
    - question_hash (str): The hash of the question.
    """
    hash_input = text + ''.join(options)
    return hashlib.md5(hash_input.encode()).hexdigest()

def hash_quiz(title, questions_data):
    """
    Generates a hash for a quiz based on its title and questions.
    
    Args:
    - title (str): The title of the quiz.
    - questions_data (list): A list of questions for the quiz.

    Returns:
    - quiz_hash (str): The hash of the quiz.
    """
    question_hashes = sorted([hash_question(q['text'], q['options']) for q in questions_data])
    hash_input = title + ''.join(question_hashes)
    return hashlib.md5(hash_input.encode()).hexdigest()

def create_quiz(title, questions_data):
    """
    Creates a new quiz or checks if a quiz already exists based on title and questions.

    Args:
    - title (str): The title of the quiz.
    - questions_data (list): A list of questions for the quiz.

    Returns:
    - quiz_id (str): The unique identifier for the created or existing quiz.
    """
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Invalid title")
    if not isinstance(questions_data, list) or not all(isinstance(q, dict) and 'text' in q and 'options' in q and 'correct_option' in q for q in questions_data):
        raise ValueError("Invalid questions data")
    
    # Generate a hash for the quiz
    quiz_hash = hash_quiz(title, questions_data)
    
    # Check if the quiz already exists in MongoDB
    existing_quiz = quizzes_collection.find_one({'hash': quiz_hash})
    if existing_quiz:
        return existing_quiz['_id']  # Return existing quiz ID
    
    # If the quiz does not exist, create a new one
    quiz_id = str(uuid.uuid4())
    quiz_data = {
        '_id': quiz_id,
        'title': title,
        'questions': [],
        'hash': quiz_hash
    }
    
    for q in questions_data:
        question_hash = hash_question(q['text'], q['options'])
        existing_question = questions_collection.find_one({'hash': question_hash})
        
        if existing_question:
            quiz_data['questions'].append(existing_question['_id'])
        else:
            question_id = create_question(q['text'], q['options'], q['correct_option'])
            quiz_data['questions'].append(question_id)
    
    quizzes_collection.insert_one(quiz_data)
    return quiz_id

def create_question(text, options, correct_option):
    """
    Creates a new question or checks if a question already exists based on its text and options.

    Args:
    - text (str): The text of the question.
    - options (list): A list of answer options.
    - correct_option (int): The index of the correct answer.

    Returns:
    - question_id (str): The unique identifier for the created or existing question.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Invalid question text")
    if not isinstance(options, list) or len(options) < 4:
        raise ValueError("Options must be a list with at least 4 options")
    if not isinstance(correct_option, int) or correct_option < 0 or correct_option >= len(options):
        raise ValueError("Invalid correct option index")

    question_hash = hash_question(text, options)
    
    existing_question = questions_collection.find_one({'hash': question_hash})
    
    if existing_question:
        return existing_question['_id']

    question_id = str(uuid.uuid4())
    question_data = {
        '_id': question_id,
        'text': text,
        'options': options,
        'correct_option': correct_option,
        'hash': question_hash
    }
    questions_collection.insert_one(question_data)
    return question_id

def submit_answer(quiz_id, question_id, user_id, selected_option):
    """
    Submits an answer for a specific question in a quiz and updates user results.

    Args:
    - quiz_id (str): The ID of the quiz.
    - question_id (str): The ID of the question.
    - user_id (str): The ID of the user.
    - selected_option (int): The selected option index.

    Returns:
    - is_correct (bool): Whether the selected answer is correct.
    - correct_option (int|None): The correct option index if the answer was incorrect; None otherwise.
    """
    if not quizzes_collection.find_one({'_id': quiz_id}):
        return None, "Quiz not found"
    if not questions_collection.find_one({'_id': question_id}):
        return None, "Question not found"
    if not isinstance(user_id, str) or not user_id.strip():
        return None, "Invalid user ID"
    if not isinstance(selected_option, int) or selected_option < 0 or selected_option >= len(questions_collection.find_one({'_id': question_id})['options']):
        return None, "Invalid selected option"

    correct_option = questions_collection.find_one({'_id': question_id})['correct_option']
    is_correct = (selected_option == correct_option)
    
    user_result = results_collection.find_one({'quiz_id': quiz_id, 'user_id': user_id})
    if not user_result:
        user_result = {
            'quiz_id': quiz_id,
            'user_id': user_id,
            'score': 0,
            'answers': []
        }

    # Check if the answer has already been submitted
    if any(answer['question_id'] == question_id for answer in user_result['answers']):
        return None, "Answer already submitted"

    user_result['answers'].append({
        'question_id': question_id,
        'selected_option': selected_option,
        'is_correct': is_correct
    })

    if is_correct:
        user_result['score'] += 1

    results_collection.replace_one({'quiz_id': quiz_id, 'user_id': user_id}, user_result, upsert=True)
    return is_correct, correct_option if not is_correct else None

def get_user_progress(quiz_id, user_id):
    """
    Fetches the progress of a user for a specific quiz.

    Args:
    - quiz_id (str): The ID of the quiz.
    - user_id (str): The ID of the user.

    Returns:
    - progress (dict): User's progress including score and answers.
    """
    user_result = results_collection.find_one({'quiz_id': quiz_id, 'user_id': user_id})
    if user_result:
        return {
            'quiz_id': quiz_id,
            'user_id': user_id,
            'score': user_result.get('score', 0),
            'answers': user_result.get('answers', [])
        }
    else:
        return {
            'quiz_id': quiz_id,
            'user_id': user_id,
            'score': 0,
            'answers': []
        }

def get_user_scores(user_id):
    """
    Fetches all historical scores for a user.

    Args:
    - user_id (str): The ID of the user.

    Returns:
    - scores (list): List of scores for each quiz.
    """
    user_results = results_collection.find({'user_id': user_id})
    scores = []
    for result in user_results:
        scores.append({
            'quiz_id': result['quiz_id'],
            'score': result.get('score', 0)
        })
    return scores
