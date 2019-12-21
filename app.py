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









    '''
    Create error handlers for all expected errors
    '''
    # handle bad request
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "message": "Bad Request, pls check your inputs"
        }), 400

    # handle unauthorized request errors
    @app.errorhandler(401)
    def unathorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": error.description,
        }), 401

    # handle forbidden requests
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "You are forbidden from accessing this resource",
        }), 403

    # handle resource not found errors
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    # handle bad request
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "message": "Something went wrong, please try again"
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
