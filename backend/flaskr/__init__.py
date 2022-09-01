import os
from xml.dom import NotFoundErr
from flask import Flask, request, abort, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in selection]
    current_questions = formatted_questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        return response
    @app.route("/")
    def index():
        return jsonify({
            "success": True,
            "message": "Welcome to the Trivia Challenge!"
        })
    
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "categories": {category.id: category.type for category in categories}
        })
    # @app.route("/categories/<int:category>")
    # def get_questions_by_category(category):
    #     questions = Question.query.filter(Question.category == category).all()
    #     if len(questions) == 0:
    #         abort(404)
    #     return questions
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()
        return jsonify({
            "success": True,
            "questions": current_questions,
            'total_questions': len(selection),
            'categories': {category.id: category.type for category in categories},
            'current_category': None
        })
    
   
    
   
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    """
    @app.route("/questions/<int:question_id>", methods=['DELETE'])
    def delete_question(question_id):
        try:
            # Filter the Question by the question_id and delete it
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            return jsonify({
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(selection)
            })
        except:
            abort(422)
    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """
    @app.route("/questions", methods=['POST'])
    def create_question():
        body = request.get_json()
        if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
            abort(422)
        the_new_question = body.get('question', None)
        the_new_answer = body.get('answer', None)
        the_new_difficulty = body.get('difficulty', None)
        the_new_category = body.get('category', None)

        try:
            question = Question(question=the_new_question, 
                                answer=the_new_answer, 
                                difficulty=the_new_difficulty, 
                                category=the_new_category)
            
            question.insert()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)


            return jsonify({
                'success': True,
                'created': question.id,
            })

        except:
            abort(422)
        finally:
            redirect('/questions')

    """
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        if search_term:
            search_results = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in search_results],
                'total_questions': len(search_results),
                'current_category': None
            })
        abort(404)

        # if search_term:
        #     selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search_term)))
        #     current_questions = paginate_questions(request, selection)
        #     return jsonify({
        #         'success': True,
        #         'questions': current_questions,
        #         'total_questions': len(selection.all()),
        #         'current_category': None
        #     })
        # else:
        #     abort(404)



    """
    @TODO:
    Create a GET endpoint to get questions based on category.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(
                Question.category == str(category_id)).all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'current_category': category_id
            })
        except:
            abort(404)
        # selection = Question.query.filter(Question.category == category_id).all()
        # current_questions = paginate_questions(request, selection)
        # if len(current_questions) == 0:
        #     abort(404)
        # return jsonify({
        #     'success': True,
        #     'questions': current_questions,
        #     'total_questions': len(selection),
        #     'current_category': category_id
        # })

    """  💩
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=['POST'])
    def play_quiz():
        try:

            body = request.get_json()

            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(422)

            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            if category['type'] == 'click':
                available_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            else:
                available_questions = Question.query.filter_by(
                    category=category['id']).filter(Question.id.notin_((previous_questions))).all()

            new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(available_questions) > 0 else None

            return jsonify({
                'success': True,
                'question': new_question
            })
        except:
            abort(422)
        # try:
        #     body = request.get_json()
        #     previous_questions = body.get('previous_questions', None)
        #     quiz_category = body.get('quiz_category', None)

        #     if quiz_category['id'] == 0:
        #         selection = Question.query.all()
        #     else:
        #         selection = Question.query.filter(
        #             Question.category == quiz_category['id']).all()

        #     if previous_questions is None:
        #         previous_questions = []
        #     else:
        #         previous_questions = [question['id'] for question in previous_questions]

        #     random_question = random.choice(selection)
        #     while random_question.id in previous_questions:
        #         random_question = random.choice(selection)
            
        #     return jsonify({
        #         'success': True,
        #         'question': random_question.format()
        #     })
        # except:
        #     abort(404)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Cannot process the request"
        })

    return app

