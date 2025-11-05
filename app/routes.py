from flask import Blueprint, request, jsonify
from .sdk import process_feedback, check_feedback_exists

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

@api_blueprint.route('/feedback', methods=['POST'])
def feedback():
    """
    Receives user feedback from the Quarkus app and
    submits it to Argilla via the SDK.
    """
    data = request.get_json()
    result = process_feedback(data)
    return jsonify(result)

@api_blueprint.route('/feedback/<report_id>/exists', methods=['GET'])
def feedback_exists(report_id):
    """
    Checks if feedback has already been submitted for a specific report ID.
    """
    exists = check_feedback_exists(report_id)
    return jsonify({"exists": exists})

def register_routes(app):
    app.register_blueprint(api_blueprint)
