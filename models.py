#import uuid


# # In-memory storage
# quizzes = {}
# questions = {}
# results = {}

# # Model Functions

# def create_quiz(title, questions_data):
#     """
#     Creates a new quiz and stores it in the in-memory storage.
    
#     Args:
#     - title (str): The title of the quiz.
#     - questions_data (list): A list of questions for the quiz, 
#       each question is a dictionary with text, options, and correct_option.
    
#     Returns:
#     - quiz_id (str): The unique identifier for the created quiz.
#     """
#     quiz_id = str(uuid.uuid4())
#     quizzes[quiz_id] = {
#         'id': quiz_id,
#         'title': title,
#         'questions': []
#     }
#     for q in questions_data:
#         question_id = create_question(q['text'], q['options'], q['correct_option'])
#         quizzes[quiz_id]['questions'].append(question_id)
#     return quiz_id

# def create_question(text, options, correct_option):
#     """
#     Creates a new question and stores it in the in-memory storage.
    
#     Args:
#     - text (str): The text of the question.
#     - options (list): A list of answer options.
#     - correct_option (int): The index of the correct answer option.
    
#     Returns:
#     - question_id (str): The unique identifier for the created question.
#     """
#     question_id = str(uuid.uuid4())
#     questions[question_id] = {
#         'id': question_id,
#         'text': text,
#         'options': options,
#         'correct_option': correct_option
#     }
#     return question_id

# def submit_answer(quiz_id, question_id, user_id, selected_option):
#     """
#     Submits an answer for a specific question in a quiz and stores the result.
    
#     Args:
#     - quiz_id (str): The unique identifier for the quiz.
#     - question_id (str): The unique identifier for the question.
#     - user_id (str): The unique identifier for the user.
#     - selected_option (int): The index of the selected answer option.
    
#     Returns:
#     - is_correct (bool): True if the selected option is correct, False otherwise.
#     - correct_answer (int or None): The correct answer index if the selected answer is incorrect.
#     """
#     if question_id not in questions or quiz_id not in quizzes:
#         return None, "Quiz or Question not found"
    
#     correct_option = questions[question_id]['correct_option']
#     is_correct = (selected_option == correct_option)
    
#     if quiz_id not in results:
#         results[quiz_id] = {}
#     if user_id not in results[quiz_id]:
#         results[quiz_id][user_id] = {
#             'score': 0,
#             'answers': []
#         }

#     results[quiz_id][user_id]['answers'].append({
#         'question_id': question_id,
#         'selected_option': selected_option,
#         'is_correct': is_correct
#     })

#     if is_correct:
#         results[quiz_id][user_id]['score'] += 1

#     return is_correct, correct_option if not is_correct else None

import uuid
import hashlib

# In-memory storage
quizzes = {}
questions = {}
results = {}

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
    
    # Check if the quiz already exists
    existing_quiz_id = next((qid for qid, qdata in quizzes.items() if qdata.get('hash') == quiz_hash), None)
    if existing_quiz_id:
        return existing_quiz_id  # Return existing quiz ID
    
    # If the quiz does not exist, create a new one
    quiz_id = str(uuid.uuid4())
    quizzes[quiz_id] = {
        'id': quiz_id,
        'title': title,
        'questions': [],
        'hash': quiz_hash
    }
    
    for q in questions_data:
        question_hash = hash_question(q['text'], q['options'])
        existing_question_id = next((qid for qid, qdata in questions.items() if qdata.get('hash') == question_hash), None)
        
        if existing_question_id:
            quizzes[quiz_id]['questions'].append(existing_question_id)
        else:
            question_id = create_question(q['text'], q['options'], q['correct_option'])
            quizzes[quiz_id]['questions'].append(question_id)
    
    return quiz_id

def create_question(text, options, correct_option):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Invalid question text")
    if not isinstance(options, list) or len(options) < 2:
        raise ValueError("Options must be a list with at least two options")
    if not isinstance(correct_option, int) or correct_option < 0 or correct_option >= len(options):
        raise ValueError("Invalid correct option index")

    question_hash = hash_question(text, options)
    
    existing_question_id = next((qid for qid, qdata in questions.items() if qdata.get('hash') == question_hash), None)
    
    if existing_question_id:
        return existing_question_id

    question_id = str(uuid.uuid4())
    questions[question_id] = {
        'id': question_id,
        'text': text,
        'options': options,
        'correct_option': correct_option,
        'hash': question_hash
    }
    return question_id

# def create_quiz(title, questions_data):
#     if not isinstance(title, str) or not title.strip():
#         raise ValueError("Invalid title")
#     if not isinstance(questions_data, list) or not all(isinstance(q, dict) and 'text' in q and 'options' in q and 'correct_option' in q for q in questions_data):
#         raise ValueError("Invalid questions data")
    
#     quiz_id = str(uuid.uuid4())
#     quizzes[quiz_id] = {
#         'id': quiz_id,
#         'title': title,
#         'questions': []
#     }
#     for q in questions_data:
#         question_id = create_question(q['text'], q['options'], q['correct_option'])
#         quizzes[quiz_id]['questions'].append(question_id)
#     return quiz_id

# def create_question(text, options, correct_option):
#     if not isinstance(text, str) or not text.strip():
#         raise ValueError("Invalid question text")
#     if not isinstance(options, list) or len(options) < 4:
#         raise ValueError("Options must be a list with at least 4 options")
#     if not isinstance(correct_option, int) or correct_option < 0 or correct_option >= len(options):
#         raise ValueError("Invalid correct option index")
    
#     question_id = str(uuid.uuid4())
#     questions[question_id] = {
#         'id': question_id,
#         'text': text,
#         'options': options,
#         'correct_option': correct_option
#     }
#     return question_id

def submit_answer(quiz_id, question_id, user_id, selected_option):
    if quiz_id not in quizzes:
        return None, "Quiz not found"
    if question_id not in questions:
        return None, "Question not found"
    if not isinstance(user_id, str) or not user_id.strip():
        return None, "Invalid user ID"
    if not isinstance(selected_option, int) or selected_option < 0 or selected_option >= len(questions[question_id]['options']):
        return None, "Invalid selected option"

    correct_option = questions[question_id]['correct_option']
    is_correct = (selected_option == correct_option)
    
    if quiz_id not in results:
        results[quiz_id] = {}
    if user_id not in results[quiz_id]:
        results[quiz_id][user_id] = {
            'score': 0,
            'answers': []
        }

    results[quiz_id][user_id]['answers'].append({
        'question_id': question_id,
        'selected_option': selected_option,
        'is_correct': is_correct
    })

    if is_correct:
        results[quiz_id][user_id]['score'] += 1

    return is_correct, correct_option if not is_correct else None
