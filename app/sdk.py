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

        # 2) Get report_id
        report_id = data.get("reportId")

        print(f"Logging feedback with id: {report_id}")

        record_dict = {
            "id": report_id,
            "response": data.get("response"),
            "thumbs": data.get("thumbs"),
            "rating": int(data.get("rating")),
            "comment": data.get("comment"),
            "assessment": data.get("assessment"),
            "reason": data.get("reason"),
            "summary": data.get("summary"),
            "qClarity": data.get("qClarity"),
            "aAgreement": data.get("aAgreement"),
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


def check_feedback_exists(reportId):
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

        # Build a filter on the record external_id (which you set via `id=reportId`)
        filter_id = Filter(("id", "==", reportId))
        query = Query(filter=filter_id)

        # Execute the query and collect matches
        matches = dataset.records(query=query).to_list(flatten=True)

        print(f"Existing feedback count for reportId {reportId}: {len(matches)}")
        return len(matches) > 0

    except Exception as e:
        current_app.logger.error(
            f"Error checking feedback for reportId '{reportId}': {e}"
        )
        return False