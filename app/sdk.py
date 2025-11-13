import argilla as rg
from argilla import Query, Filter
from flask import current_app


def init_argilla(app):
    """
    Initialize the Argilla SDK client once at app startup,
    pointing at the configured workspace.
    """
    print("Initializing Argilla SDK...")

    app.argilla_client = rg.Argilla(
        api_url=app.config['ARGILLA_API_URL'],
        api_key=app.config['ARGILLA_API_KEY'],
    )
    print("Done Initializing Argilla SDK...")


def process_feedback(data):

    try:
        client = current_app.argilla_client
        ws = current_app.config['ARGILLA_WORKSPACE']
        ds_name = current_app.config['ARGILLA_DATASET']

        # 1) Load your pre‑created dataset
        dataset = client.datasets(name=ds_name, workspace=ws)
        if dataset is None:
            return {
                "status": "error",
                "message": f"Dataset '{ds_name}' not found in workspace '{ws}'",
                "data": data
            }

        # 2) Get report_id (handle both report_id and reportId from client)
        report_id = data.get("report_id") or data.get("reportId")

        record_dict = {
            "id": report_id,
            "response": data.get("response"),
            "rating": int(data.get("rating")),
            "comment": data.get("comment"),
            "accuracy": data.get("accuracy"),
            "reasoning": data.get("reasoning"),
            "checklist": data.get("checklist"),
        }

        # 4) Log the Record using Dictionary
        dataset.records.log([record_dict])

        return {
            "status": "success",
            "data": data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": data
        }


def check_feedback_exists(report_id):
    """
    Checks if feedback has already been submitted for a given report ID in Argilla,
    by querying on the record external_id.
    """
    try:
        client = current_app.argilla_client
        ws = current_app.config["ARGILLA_WORKSPACE"]
        ds_name = current_app.config["ARGILLA_DATASET"]

        print(f"Connecting to Argilla: Workspace={ws}, Dataset={ds_name}")

        # Load the dataset
        dataset = client.datasets(name=ds_name, workspace=ws)
        if not dataset:
            print("Dataset not found.")
            return False

        # Build a filter on the record external_id (which you set via `id=report_id`)
        filter_id = Filter(("id", "==", report_id))
        query = Query(filter=filter_id)

        # Execute the query and collect matches
        matches = dataset.records(query=query).to_list(flatten=True)

        print(f"Existing feedback count for report_id {report_id}: {len(matches)}")
        return len(matches) > 0

    except Exception as e:
        current_app.logger.error(
            f"Error checking feedback for report_id '{report_id}': {e}"
        )
        return False