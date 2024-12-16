# AI-Orchestration Platform

## Project Vision

Our platform aims to transform workforce perception by empowering professionals to create AI assistants tailored to their roles. These assistants optimize efficiency, decision-making, and overall performance by aligning with specific tasks and workflows. Through a hierarchical framework, we enable better representation of responsibility levels within any team, enhancing the effectiveness of AI assistants.

The platform allows users to create customized AI assistants, structured according to a **hierarchical framework** that mirrors real-world teams, roles, and tasks. From team-specific objectives to individual tasks, the hierarchy supports real-time performance tracking, metrics-based optimization, and dynamic feedback loops.

---

## Folder Structure

```plaintext
src/
├── controllers/
├── domain/
├── infrastructure/
├── use_cases/
├── tests/
├── app.py
├── config.py
.env
.env.sample
.gcloudignore
.gitignore
Dockerfile
README.md
requirements.txt
```
### **1. `controllers/`**

Handles incoming HTTP requests, routes them to the appropriate use cases, and validates input. Controllers also generate responses based on use case outcomes.

### **2. `domain/`**

The **core business logic** layer. It contains entities, exceptions, and business rules foundational to the application.

- **Entities**: Represent essential business objects like `Customer` and `Order`, designed without dependencies on external services.
- **Exceptions**: Custom exception classes (e.g., `CustomerNotFoundException`) that ensure consistent error handling across the application.

```plaintext
domain/
├── entities/
│   ├── customer.py
│   ├── order.py
├── exceptions.py
```
### **3. `infrastructure/`**

This layer manages communication with external systems, such as databases and third-party APIs, housing concrete implementations of repository interfaces used in the domain.

### **4. `use_cases/`**

Encapsulates application-specific business rules, orchestrating data flow between entities and infrastructure. Examples include:

- **User Registration**: Validates input, creates a user entity, and saves it to the database.

### **5. `app.py`**

Main application file, responsible for initializing the application, setting up routes, loading environment variables, and connecting dependencies like databases or external APIs.

### **6. `config.py`**

Defines configuration settings, such as environment variables and external service URLs. Configures the application for development, staging, or production environments.

### **7. `.env`**

Stores sensitive environment variables (e.g., API keys, database URIs). Ensure that `.env` is **not pushed to version control**.

### **8. `.gcloudignore`**

Specifies which files/folders to exclude when deploying to Google Cloud, avoiding unnecessary files from being uploaded during deployment.

### **9. `Dockerfile`**

Defines the environment for a Docker container to ensure consistent application behavior across environments.

### **10. `requirements.txt`**

Lists the Python packages and dependencies required by the project.
---

## Running the Application

### Using Python Virtual Environment (Recommended)

1. Set up a virtual environment:
   ```bash
   python3 -m venv venv  # If this fails, try python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```
 <h2>Running the Application</h2>

    <h3>Using Python Virtual Environment (Recommended)</h3>
    <p>Set up a virtual environment:</p>
    <pre><code>python3 -m venv venv  # If this fails, try python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate</code></pre>

    <p>Install dependencies:</p>
    <pre><code>pip install -r requirements.txt</code></pre>

    <p>Set up environment variables:</p>
    <pre><code>cp .env.sample .env
# Edit .env with the required values.</code></pre>

    <p>Run the application:</p>
    <pre><code>python src/app.py</code></pre>

    <h3>Using Docker</h3>
    <p>Build the Docker image:</p>
    <pre><code>docker build -t ai-orchestration-platform .</code></pre>

    <p>Run the container:</p>
    <pre><code>docker run -p 5000:5000 ai-orchestration-platform</code></pre>

    <h3>Running Tests</h3>
    <p>The project includes unit tests for the core components in the domain and use_cases layers.</p>
    <pre><code>python -m unittest discover -s tests</code></pre>

    <h2>Deployment</h2>
    <p>The project is currently deployed on Render. Ensure <code>.gcloudignore</code> is set up to exclude unnecessary files for future deployments on Google Cloud Platform (GCP).</p>

    <h3>Initialize Google Cloud SDK (for later use):</h3>
    <pre><code>gcloud init</code></pre>

    <h3>Deploy to Google Cloud (for later use):</h3>
    <pre><code>gcloud app deploy</code></pre>

# Render Deployment Guide for Agent Square Project

## Overview

This document outlines the steps necessary to deploy the Agent Square project on the Render platform. Render is a cloud platform that simplifies the deployment of web services.

## General Steps to Deploy on Render

1. **Create a Render Account**: 
   - Visit [Render](https://render.com) and create an account if you haven’t already.

2. **Connect a Git Repository**:
   - Link your Render account to a Git provider (GitHub, GitLab, or Bitbucket).
   - Choose the repository that contains your project.

3. **Create a New Web Service**:
   - Select `New > Web Service` from the Render dashboard.
   - Configure your service by selecting the repository, branch, and instance type (Free or paid based on your requirements).
   - Define the Root Directory (if deploying from a subdirectory).

4. **Define Build and Start Commands**:
   - Specify the Build Command to install dependencies.
   - Define the Start Command to run the application.

5. **Configure Environment Variables (if needed)**:
   - Add any environment variables required by the application.
   - You can manage these in the Environment tab of your service.

6. **Configure Health Checks**:
   - Set up a Health Check Path to help Render monitor your service’s status.

7. **Deploy Automatically or Manually**:
   - Enable Auto-Deploy to deploy automatically when you push updates to your chosen branch. Otherwise, you can manually trigger deployments.

8. **Custom Domain Setup (optional)**:
   - Configure a custom domain if required.

9. **Notifications and Maintenance Mode (optional)**:
   - Configure notifications for deployment statuses.
   - Enable Maintenance Mode when needed.

## Project-Specific Deployment Instructions

### Repository and Branch Configuration

- **Repository**: This project is linked to a GitLab repository at [https://gitlab.com/Haileamlak/agent-square](https://gitlab.com/Haileamlak/agent-square).
- **Branch**: The deployment branch specified is `mihret.deploy_render`.

### Root Directory

- Set the Root Directory to `backend/src` since the code for this service is located here. Changes outside of this directory won’t trigger auto-deploys, which is useful for monorepo setups.

### Build Command

- Use the command below to install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
- **Using pip freeze for Dependencies**: To ensure all dependencies are included in `requirements.txt`, run:
    ```bash
    pip freeze > src/requirements.txt
    ```
- Using `pip freeze` is recommended as it captures any packages that might have been missed when adding dependencies manually.

### Start Command

- The app uses Gunicorn as its web server. For this service, due to extended processing times, a higher timeout is set:
    ```bash
    gunicorn app:app --timeout 300 --log-file -
    ```
- The `--timeout 300` flag increases the timeout period to 300 seconds, allowing for longer-running requests.
- Log File: Use `--log-file -` to enable logging, which helps capture any issues that occur during deployment or runtime. Refer to the official [Gunicorn documentation](https://docs.gunicorn.org/) for additional configuration options.

### Adding Cloud Access Key as a Secret

- To enable access to Google Cloud services, add `cloud-access-key.json` as a secret file in the Advanced settings on Render.
- After uploading the file, the path will be provided as `/etc/render/secret/cloud-access-key.json`.
- Define the path for the Google credentials by setting the environment variable:
    ```
    GOOGLE_APPLICATION_CREDENTIALS=/etc/render/secret/cloud-access-key.json
    ```
- Ensure you update the environment variable path to point to this location on Render.

### Health Check Path

- To monitor the health of the application, set the Health Check Path to `/healthz`.

### Auto-Deploy and Notifications

- Enable Auto-Deploy for automatic deployment upon code updates.
- Notifications are configured to follow the default workspace settings (only failures are notified).

## Conclusion

Following these steps will help you successfully deploy the Agent Square project on Render. Ensure to monitor the deployment and application health through the Render dashboard.
## Platform Hierarchy

### Customizable AI Assistants by Team

The platform structures assistants using a hierarchical framework:

- **Team Level**: Represents functional teams, allowing businesses to organize assistants by operation areas like tech, HR, or customer support.
- **Agent Level**: Agents within teams design assistants for role-specific tasks, improving role alignment and efficiency.
- **Goal and Sub-Goal Levels**: High-level goals set by agents break down into focused sub-goals, facilitating targeted metrics.
- **Workstream Level**: Concrete tasks within sub-goals, detailing step-by-step actions to meet objectives.
- **Module and Function Levels**: Granular tasks and API integrations that enable the assistant to meet larger goals effectively.

### Performance Tracking and Feedback

Each assistant, whether custom-built or pre-configured, has integrated real-time metrics and feedback. Metrics such as time-to-hire and customer response rates are automatically logged, with user feedback guiding dynamic adjustments to maximize effectiveness.

#### Metric Levels:

- **Agent Metrics**: Evaluate individual productivity and interaction quality.
- **Goal Metrics**: Measure success against each major objective, like sourcing candidates.
- **Sub-Goal and Workstream Metrics**: Track efficiency at a more detailed level.
- **Module and Function Metrics**: Ensure accurate task execution and API reliability.

## Technologies Used

- **Python**: Core programming language.
- **Flask**: Lightweight web framework for building APIs.
- **Google Cloud**: For deployment and cloud services integration (future use).
- **Render**: For deployment
- **Docker**: For containerization.
- **Clean Architecture**: For structuring the application.# agent4hire_backend
# agent4hire_backend
# agent4hire_backend
# agent4hire_backend
# agent4hire_backend
# agent4hire_backend
# agent4hire_backend
