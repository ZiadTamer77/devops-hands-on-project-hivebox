> This project is part of a DevOps hands-on learning roadmap focusing on DevOps Fundamentals

## Implementation



### Phase 1 — Preparation

#### Objective

Set up the repository and establish a proper Git workflow using feature branches and pull requests.

---

### Steps Performed

#### 1. Forked the Repository

Forked the original HiveBox repository to my GitHub account to create an independent working copy.

---

#### 2. Cloned the Repository Locally

```bash
git clone https://github.com/ZiadTamer77/devops-hands-on-project-hivebox.git
cd devops-hands-on-project-hivebox
```

---

#### 3. Created a Feature Branch

```bash
git checkout -b phase-1-preparation
```

👉 This ensures changes are isolated from the `main` branch.

---

#### 4. Followed Git Workflow Best Practices

* No direct commits to `main`
* All changes are made via feature branches
* Changes will be merged through Pull Requests

---

### Outcome

* Local development environment ready
* Git workflow established
* Repository prepared for structured development

### Phase 2 - Application Versioning & Containerization

# Version App (Dockerized)

Building on the Git workflow established in Phase 1, this phase focuses on implementing application versioning and containerization.

## Overview

This is a simple Python application that prints the current application version.

The application is containerized using Docker and follows a CLI-style execution pattern.

---

#### Objective

Implement application versioning using semantic versioning principles and containerize the application using Docker.

### Steps Performed

#### 1. Implemented Versioning Logic
- Created a central version file (`version.py`)
- Defined application version using semantic versioning

#### 2. Developed CLI Functionality
- Implemented a function to print the application version
- Added support for `--version` flag

#### 3. Containerized the Application
- Created a Dockerfile
- Configured container to run the application as a CLI tool

## Why This Matters

Versioning is critical in software delivery pipelines. It enables:

- Tracking application changes
- Tagging Docker images
- Managing deployments across environments

This implementation serves as a foundation for integrating versioning into CI/CD workflows.

## Project Structure

```
.
├── Dockerfile
├── main.py
├── version.py
```

---

## Prerequisites

* Docker installed on your system

Verify Docker:

```bash
docker --version
```

---

## Build the Docker Image

From the project root directory:

```bash
docker build -t version-app .
```

---

## Run the Application

Execute the container:

```bash
docker run --rm version-app
```

### Expected Output

```
0.0.1
```

---

## Explanation

* The container runs a Python script (`main.py`)
* The script checks for the `--version` flag
* It prints the version defined in `version.py`
* The container exits immediately after execution

---

## Notes

* The `--rm` flag removes the container after execution
* This is a short-lived container (CLI-style), not a long-running service
* No ports are exposed because this is not a web application

---

## Development Notes

To change the version:

Edit:

```python
# version.py
VERSION = "0.0.1"
```

Then rebuild the image:

```bash
docker build -t version-app .
```

---

## Key Concepts Demonstrated

* Docker image creation
* Container execution
* CLI-based container design
* Separation of concerns (version defined centrally)

---

---

## Phase 3 — API Development & Testing

### Objective

Transform the application from a CLI-based tool into a testable HTTP service by exposing the application version through an API endpoint and validating it with automated tests.

---

### Overview

In this phase, the application was extended to provide a REST API using Flask.
The `/version` endpoint exposes the application version in JSON format, making it suitable for integration with CI/CD pipelines and external systems.

---

### Steps Performed

#### 1. Introduced Flask Application

* Created a Flask application using the application factory pattern
* Structured the project into layers:

  * `routes/` → HTTP layer
  * `services/` → business logic
* Ensured separation of concerns for better testability and maintainability

---

#### 2. Implemented `/version` Endpoint

```http
GET /version
```

**Response:**

```json
{
  "version": "0.0.1"
}
```

* No input parameters required
* Deterministic response
* Designed for automation and monitoring use cases

---

#### 3. Refactored Business Logic

* Moved version logic into a service layer:

```python
def get_version():
    return VERSION
```

* Ensured:

  * Reusability across CLI and API
  * Testability independent of Flask

---

#### 4. Implemented Unit & API Tests

Two levels of testing were introduced:

##### Service-Level Test

```python
from app.services.version_service import get_version

def test_get_version():
    assert get_version() == "0.0.1"
```

---

##### API-Level Test

```python
def test_version_endpoint(client):
    response = client.get("/version")

    assert response.status_code == 200
    assert response.get_json() == {"version": "0.0.1"}
```

---

### Testing Strategy

* **Unit tests** validate business logic independently
* **API tests** validate HTTP behavior and integration
* Designed to run in CI pipelines without requiring a running server

---

### Why This Matters

Exposing application functionality via an API enables:

* Integration with monitoring systems
* Automated validation in CI/CD pipelines
* Standardized communication between services

Testing ensures:

* Reliability of deployments
* Early detection of regressions
* Confidence in automation workflows

---

### Outcome

* Application evolved from CLI tool → HTTP service
* `/version` endpoint implemented and tested
* Codebase structured for scalability and CI integration
* Foundation prepared for future endpoints (e.g., `/temperature`)

---

## Author

Zeyad Tamer
