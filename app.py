from flask import Flask
from flask_restful import Api
from resources import CreateQuiz, GetQuiz, SubmitAnswer, GetResults, ListQuizzes

# Initialize Flask app and API
app = Flask(__name__)
api = Api(app)

# Define the API endpoints
api.add_resource(CreateQuiz, '/quiz/')
api.add_resource(GetQuiz, '/quiz/<string:quiz_id>/')
api.add_resource(SubmitAnswer, '/quiz/<string:quiz_id>/question/<string:question_id>/answer/')
api.add_resource(GetResults, '/quiz/<string:quiz_id>/result/<string:user_id>/')
api.add_resource(ListQuizzes, '/quizzes/')

if __name__ == '__main__':
    app.run(debug=True)
