# SPDX-FileCopyrightText: Copyright (c) 2025, Red Hat Inc. & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
