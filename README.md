# Morpheus Feedback API

The **Morpheus Feedback API** is a Python Flask-based microservice designed to serve as an integration layer between the Quarkus-based Morpheus application and the Argilla backend. Its primary goal is to accept user feedback data from the Morpheus clients and forward it to the hosted Argilla instance using the Argilla Python SDK.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation and Setup](#installation-and-setup)
- [Running Locally](#running-locally)
- [Deployment](#deployment)

---

## Features

- **Clean Separation of Concerns:** The Flask service encapsulates all Argilla-specific interactions.
- **Scalability & Extensibility:** Built using the application factory pattern, allowing easy expansion (e.g., additional endpoints or services).
- **Containerization Ready:** Comes with a Dockerfile and OpenShift deployment manifests for streamlined container-based deployment.
- **Secure Integration:** Sensitive configurations (like API keys) can be managed using environment variables or OpenShift Secrets.
- **Unit Tested:** Basic tests are provided to ensure the API endpoint operates as expected.

---

## Architecture Overview

The Morpheus Feedback API is designed as part of a multi-container Pod on OpenShift. The Pod includes:

- **Flask Service:** Serves as the external entry point for feedback data.
- **Argilla Server & Dependencies:** The Argilla backend (including Argilla Server, Worker, Redis, PostgreSQL, and Elasticsearch) runs as sidecar containers.
- **Internal Communication:** All containers communicate over the Pod’s local network, limiting external exposure.

---

## Project Structure

```plaintext
Morpheus Feedback API
├── app/                   # Flask application code
│   ├── __init__.py        # Application factory
│   ├── routes.py          # API route definitions
│   ├── services.py        # Argilla communication logic
│   ├── sdk.py             # Argilla SDK wrapper and utilities
│   └── config.py          # Configuration management
├── deploy/                # OpenShift deployment manifests
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── run.py                 # Flask entrypoint
├── tests/                 # Unit tests for the API
└── README.md              # Project documentation
```

---

## Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose (optional for containerized setup)
- Access to an Argilla instance (local or hosted)
- OpenShift (for production deployment)

---

## Installation and Setup

1. Clone the Repository:
   ```
   git clone https://github.com/your-repo/morpheus-feedback-api.git
   cd morpheus-feedback-api
   ```
2. Create a Virtual Environment:

   ```
   python -m venv venv
   source venv/bin/activate

   ```

3. Set Up Configuration:

   Update `config.py` file with the following variables:

   ```python
   ARGILLA_API_URL = <your-argilla-api-url>
   ARGILLA_API_KEY = <your-argilla-api-key>
   ARGILLA_DATASET = <your-argilla-dataset>
   ARGILLA_WORKSPACE = <your-argilla-workspace>
   ```

---

## Running Locally

1. Install Dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set Up Argilla Container:

   Create a Docker network for Argilla:

   ```bash
   docker network create argilla-net
   ```

   Start Elasticsearch container:

   ```bash
   docker run -d --name elasticsearch-for-argilla --network argilla-net \
     -p 9200:9200 -p 9300:9300 \
     -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
     -e "discovery.type=single-node" \
     -e "xpack.security.enabled=false" \
     docker.elastic.co/elasticsearch/elasticsearch:8.5.3
   ```

   Start Argilla Quickstart container:

   ```bash
   docker run -d --network argilla-net \
     -e "ARGILLA_ELASTICSEARCH=http://localhost:9200" \
     --name quickstart -p 6900:6900 \
     argilla/argilla-quickstart:latest
   ```

   **Note:** Make sure you have both `quickstart` and `elasticsearch-for-argilla` containers running.
   See https://docs.argilla.io/v2.0/getting_started/quickstart/ for more details.

3. Access Argilla UI:

   Open your browser and navigate to:

   ```
   http://localhost:6900/sign-in
   ```

4. Start the Flask Service:

   ```bash
   python run.py
   ```

5. Access the API:

   Visit `http://localhost:5001` to access the API.

---


## Deployment


1. If a namespace does not exist, create one::

   ```bash
   export YOUR_NAMESPACE=yourNamespaceNameHere
   oc new-project $YOUR_NAMESPACE
   ```

2. Create an image pull secret to authorize pulling the ExploitIQ container image:

   ```bash
   oc create secret generic exploit-iq-pull-secret --from-file=.dockerconfigjson=<path/to/.docker/config.json> --type=kubernetes.io/dockerconfigjson
   ```

3. Deploy to OpenShift:

   ```bash
   oc apply -f deploy -n $YOUR_NAMESPACE
   ```