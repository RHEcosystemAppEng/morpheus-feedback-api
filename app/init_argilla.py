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
                name="assessment",
                title="Do you agree with the final assessment of the vulnerability?",
                labels=[
                    "Yes, it is clear and well-supported.",
                    "Mostly, but some critical aspects are missing.",
                    "Partially, the evidence is weak or contradictory.",
                    "No, it is incorrect or unsupported.",
                ],
                required=True
            ),
            rg.LabelQuestion(
                name="reason",
                title="Is the reason for classifying the CVE clear and well-supported?",
                labels=[
                    "Yes, it is clear and well-supported.",
                    "Mostly, but some critical aspects are missing.",
                    "Partially, the evidence is weak or contradictory.",
                    "No, it is incorrect or unsupported.",
                ],
                required=True
            ),
            rg.LabelQuestion(
                name="summary",
                title="Does the summary accurately capture the key findings and conclusions?",
                labels=[
                    "Yes, it is clear and well-supported.",
                    "Mostly, but some critical aspects are missing.",
                    "Partially, the evidence is weak or contradictory.",
                    "No, it is incorrect or unsupported.",
                ],
                required=True
            ),
            rg.LabelQuestion(
                name="q_clarity",
                title="Were the checklist questions clear and understandable?",
                labels=[
                    "Yes, it is clear and well-supported.",
                    "Mostly, but some critical aspects are missing.",
                    "Partially, the evidence is weak or contradictory.",
                    "No, it is incorrect or unsupported.",
                ],
                required=True
            ),
            rg.LabelQuestion(
                name="a_agreement",
                title="Do you agree with the answers provided for the checklist questions?",
                labels=[
                    "Yes, it is clear and well-supported.",
                    "Mostly, but some critical aspects are missing.",
                    "Partially, the evidence is weak or contradictory.",
                    "No, it is incorrect or unsupported.",
                ],
                required=True
            ),
            rg.LabelQuestion(
                name="thumbs",
                title="Do you like this response?",
                labels=["👍", "👎"],
                required=True
            ),
            rg.RatingQuestion(
                name="rating",
                title="Rate the response quality",
                values=[1, 2, 3, 4, 5],
                required=False
            ),
            rg.TextQuestion(
                name="comment",
                title="Any suggestions or comments?",
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