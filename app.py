import os
from flask_cors import CORS
from flask import Flask, jsonify, abort, request
from models import setup_db, db, Movie, Actor
from auth.auth import AuthError, requires_auth
from validate import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def welcome():
        try:
            return 'Welcome to Capstone Hub!'
        except:
            abort(500)











    # handle bad request
    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "message": "Something went wrong, please try again"
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
