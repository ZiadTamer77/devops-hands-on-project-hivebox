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

## Author

Zeyad Tamer
