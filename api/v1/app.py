#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_cors import CORS
from api.v1.views import app_views
from models import db, app


CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)

@app.teardown_appcontext
def tear_down_db(exc):
    """
    The function `tear_down_db` closes the database session.
    """
    db.session.close()


@app.errorhandler(404)
def error_404(err):
    """
    returns a response with a JSON object with an error message
    for a 404 Not Found status code.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    # use env var for the host and port 
    app.run(host='0.0.0.0',
            port=5000, debug=True)
