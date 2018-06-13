from app import app
from flask import jsonify


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "error": "Bad request", "message": 
        "Make sure JSON data is in the correct format"}), 400


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "error": "Page not found", 
        "message": "Enter correct URL"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"error": "Internal server error"}), 500
    