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
