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

from flask import Flask
from .init_argilla import create_workspace, create_dataset
from .routes import register_routes
from .sdk import init_argilla


def create_app():
    app = Flask(__name__)

    # Load configuration from app/config.py
    app.config.from_object('app.config.Config')

    # Store flag on the app object
    app._argilla_initialized = False

    init_argilla(app)
    print("Argilla SDK initialized successfully.")

    @app.before_request
    def bootstrap_argilla():
        if not app._argilla_initialized:
            app._argilla_initialized = True
            print("Creating Argilla workspace and dataset...")
            create_workspace(
                api_url=app.config["ARGILLA_API_URL"],
                api_key=app.config["ARGILLA_API_KEY"],
                name=app.config["ARGILLA_WORKSPACE"]
            )
            create_dataset(
                api_url=app.config["ARGILLA_API_URL"],
                api_key=app.config["ARGILLA_API_KEY"],
                workspace=app.config["ARGILLA_WORKSPACE"],
                dataset_name=app.config["ARGILLA_DATASET"]
            )
        else:
            print("Argilla already initialized, skipping...")

    register_routes(app)
    return app
