from flask import request

from pyard import ARD
from pyard.exceptions import PyArdError

# Globally accessible for all endpoints
ard = ARD()


def redux_controller():
    if request.json:
        # Check the request has required inputs
        try:
            gl_string = request.json["gl_string"]
            reduction_method = request.json["reduction_method"]
        except KeyError:
            return {"message": "gl_string and reduction_method not provided"}, 400
        # Perform redux
        try:
            redux_gl_string = ard.redux_gl(gl_string, reduction_method)
            return {"ard": redux_gl_string}, 200
        except PyArdError as e:
            return {"message": e.message}, 400

    # if no data is sent
    return {"message": "No input data provided"}, 404
