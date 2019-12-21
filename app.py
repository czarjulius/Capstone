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
  return 'Welcome to Capstone Hub!'

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)