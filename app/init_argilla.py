import argilla as rg


def create_workspace(api_url: str, api_key: str, name: str):
    client = rg.Argilla(api_url=api_url, api_key=api_key)
    try:
        workspace_to_create = rg.Workspace(name=name)
        created_workspace = workspace_to_create.create()
        print(f"Workspace '{name}' created successfully")
    except Exception as e:
        print(f"Workspace '{name}' exists or failed to create: {e}")


def create_dataset(api_url: str, api_key: str, workspace: str, dataset_name: str):
    client = rg.Argilla(api_url=api_url, api_key=api_key)

    # Define the dataset settings
    settings = rg.Settings(
        guidelines="Please provide feedback to help us improve AI responses.",
        fields=[
            rg.TextField(name="response", title="AI Response"),
        ],
        questions=[
            rg.LabelQuestion(
                name="question1",
                title="How accurate do you find ExploitIQ's assessment?",
                labels=[
                    "Very Accurate",
                    "Mostly Accurate",
                    "Somewhat Inaccurate",
                    "Incorrect",
                ],
                required=True
            ),
            rg.LabelQuestion(
                name="question2",
                title="Is the reasoning and summary of findings clear, complete, and well-supported?",
                labels=[
                    "Yes",
                    "Mostly",
                    "Somewhat",
                    "No",
                ],
                required=True
            ),
            rg.LabelQuestion(
                name="question3",
                title="Were the checklist questions and explanations easy to understand?",
                labels=[
                    "Yes",
                    "Mostly",
                    "Somewhat",
                    "No",
                ],
                required=True
            ),
            rg.RatingQuestion(
                name="rating",
                title="Rate the response (1 = Poor, 5 = Excellent):",
                values=[1, 2, 3, 4, 5],
                required=True
            ),
            rg.TextQuestion(
                name="comment",
                title="Do you have any additional feedback or suggestions to improve the analysis?",
                use_markdown=True,
                required=False
            )
        ],
        metadata=[
            rg.TermsMetadataProperty(
                name="report_id",
                title="Report ID",
            )
        ],
        allow_extra_metadata=True
    )

    try:
        # Create the dataset with a custom name
        dataset = rg.Dataset(
            workspace=workspace,
            name=dataset_name,
            settings=settings,
        )

        # Create the dataset in Argilla instance
        dataset.create()
        print(f"Dataset '{dataset_name}' created successfully in workspace '{workspace}'")
    except Exception as e:
        print(f"Dataset '{dataset_name}' exists or failed to create: {e}")