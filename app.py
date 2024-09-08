from flask import Flask
from flask_restful import Api
from pymongo import MongoClient
from resources import CreateQuiz, GetQuiz, SubmitAnswer, GetResults, ListQuizzes

# Initialize Flask app
app = Flask(__name__)
api = Api(app)

# Connect to MongoDB
client = MongoClient('mongodb://mongo:27017/')  # Use 'mongo' as the hostname to connect to the MongoDB container
db = client['quiz_db']  # Database name

# Pass the db instance to resources
api.add_resource(CreateQuiz, '/quiz/', resource_class_kwargs={'db': db})
api.add_resource(GetQuiz, '/quiz/<string:quiz_id>/', resource_class_kwargs={'db': db})
api.add_resource(SubmitAnswer, '/quiz/<string:quiz_id>/question/<string:question_id>/answer/', resource_class_kwargs={'db': db})
api.add_resource(GetResults, '/quiz/<string:quiz_id>/result/<string:user_id>/', resource_class_kwargs={'db': db})
api.add_resource(ListQuizzes, '/quizzes/', resource_class_kwargs={'db': db})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
