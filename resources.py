from flask_restful import Resource, reqparse
from models import quizzes_collection, questions_collection, results_collection, create_quiz, submit_answer

# Parser for creating a new quiz
quiz_parser = reqparse.RequestParser()
quiz_parser.add_argument('title', type=str, required=True, help="Title of the quiz is required")
quiz_parser.add_argument('questions', type=list, location='json', required=True, help="Questions for the quiz are required")

# Parser for submitting an answer
answer_parser = reqparse.RequestParser()
answer_parser.add_argument('selected_option', type=int, required=True, help="Selected option is required")

class CreateQuiz(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def post(self):
        """
        Endpoint to create a new quiz.
        """
        try:
            args = quiz_parser.parse_args()
            quiz_id = create_quiz(args['title'], args['questions'])
            return {'quiz_id': quiz_id}, 201
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': 'An unexpected error occurred: ' + str(e)}, 500

class GetQuiz(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def get(self, quiz_id):
        """
        Endpoint to fetch a quiz by its ID.
        """
        quiz = quizzes_collection.find_one({'_id': quiz_id})
        if not quiz:
            return {'message': 'Quiz not found'}, 404

        quiz_data = {
            'id': quiz['_id'],
            'title': quiz['title'],
            'questions': [
                {
                    'id': q_id,
                    'text': questions_collection.find_one({'_id': q_id})['text'],
                    'options': questions_collection.find_one({'_id': q_id})['options']
                }
                for q_id in quiz['questions']
            ]
        }
        return quiz_data, 200

class SubmitAnswer(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def post(self, quiz_id, question_id):
        """
        Endpoint to submit an answer for a specific question in a quiz.
        """
        user_id = reqparse.request.headers.get('User-ID')
        if not user_id:
            return {'message': 'User ID is required in headers'}, 400
        
        try:
            args = answer_parser.parse_args()
            is_correct, correct_answer = submit_answer(quiz_id, question_id, user_id, args['selected_option'])
            if is_correct is None:
                return {'message': correct_answer}, 404
            return {'correct': is_correct, 'correct_answer': correct_answer}, 200
        except ValueError as e:
            return {'message': str(e)}, 400
        except Exception as e:
            return {'message': 'An unexpected error occurred: ' + str(e)}, 500

class GetResults(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def get(self, quiz_id, user_id):
        """
        Endpoint to get the user's results for a specific quiz.
        """
        user_result = results_collection.find_one({'quiz_id': quiz_id, 'user_id': user_id})
        if not user_result:
            return {'message': 'Results not found'}, 404

        return {
            'User-ID': user_id,
            'quiz_id': quiz_id,
            'score': user_result['score'],
            'answers': user_result['answers']
        }, 200

class ListQuizzes(Resource):
    def __init__(self, **kwargs):
        self.db = kwargs['db']

    def get(self):
        """
        Endpoint to list all quiz IDs.
        """
        quiz_ids = [quiz['_id'] for quiz in quizzes_collection.find()]
        return {'quiz_ids': quiz_ids}, 200
