NASA Flask App
Overview
The NASA Flask App is a simple web application designed to showcase data from NASA's public APIs. This project integrates Flask, a micro web framework for Python, to serve dynamic content, process API responses, and provide a clean and user-friendly interface for users to explore NASA-related data.

This repository contains all the necessary files for building and deploying the app using Docker and Kubernetes. The application includes a Horizontal Pod Autoscaler (HPA) setup, an ingress controller for routing, and is optimized for high availability and scaling in Kubernetes.

Table of Contents
Features
Requirements
Installation
Running the Application
Kubernetes Deployment
CI/CD Integration
Testing
Contributing
License
Features
NASA Data Fetching: The application connects to NASA's public APIs to retrieve various datasets, such as images, Mars rover data, and more.
Flask Framework: Built on the Flask framework for flexibility and simplicity.
Gunicorn Server: Gunicorn is used as the production server for handling multiple requests efficiently.
Docker & Kubernetes Ready: Packaged as a Docker container and ready to be deployed on a Kubernetes cluster with auto-scaling, ingress, and service management.
Horizontal Pod Autoscaling (HPA): Adjusts the number of pods in the Kubernetes cluster based on CPU utilization.
API First: The app serves JSON responses as well as a web interface.
Requirements
To run the application, you need the following:

Python 3.9+
Flask: A lightweight WSGI web application framework.
Docker: Containerize the application for ease of deployment.
Kubernetes: Orchestrates and manages the deployment, scaling, and operations of the app.
kubectl: Command-line interface for running commands against Kubernetes clusters.
Helm: Used for managing Kubernetes applications.
ArgoCD (optional): For automated deployment and GitOps-based workflows.
External Libraries:

Requests
pymongo
prometheus-flask-exporter (for Prometheus metrics)
Installation
Clone the Repository


git clone https://github.com/your-username/nasa-flask-app.git
cd nasa-flask-app
Set Up Virtual Environment (Optional)


python3 -m venv venv
source venv/bin/activate
Install Dependencies
Install the required Python libraries from the requirements.txt file.



pip install -r requirements.txt
Running the Application
Running Locally
Set environment variables (optionally using .env files).

Copy .env.example to .env and modify accordingly.
Run the Flask App:



flask run
This starts the app on http://localhost:5000.

Docker
Build the Docker Image:



docker build -t nasa-flask-app .
Run the Docker Container:



docker run -p 5000:5000 nasa-flask-app
The application will be accessible at http://localhost:5000.

Kubernetes Deployment
Prerequisites
A running Kubernetes cluster (e.g., Minikube, AWS EKS, GKE).
kubectl and Helm installed on your local machine.
Metrics Server deployed in the cluster for HPA.
Deploying with Helm
Add Helm Repository:



helm repo add nasa-flask-app https://charts.yourdomain.com
helm repo update
Install the Application:



helm install nasa-flask-app nasa-flask-app/nasa-flask-app-chart
Access the App: If using Minikube, you can access the app via the ingress at http://<minikube-ip>.

Horizontal Pod Autoscaler (HPA)
The app comes with HPA pre-configured. It automatically scales based on CPU utilization.

To check the HPA:



kubectl get hpa
CI/CD Integration
This project integrates with ArgoCD for continuous deployment. By committing changes to the Git repository, ArgoCD will automatically sync and deploy the changes to the Kubernetes cluster.

For CI pipelines, consider using GitHub Actions or Jenkins for static code analysis (SonarQube), vulnerability scans (Trivy), and automated testing.

Testing
To ensure the app works as expected, you can use Flask’s built-in testing framework along with other tools like pytest:

Run Unit Tests:



pytest
Test Endpoints with Curl:



curl http://localhost:5000/api/data
Contributing
Fork the repository.
Create a new branch.
Submit a pull request.
All contributions are welcome. For more information, check the CONTRIBUTING.md file.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Additional Notes
SonarQube: This project integrates SonarQube for static code analysis. Ensure the SonarQube server is running, and configure the sonar-project.properties file for correct analysis.
Trivy: Security scanning is integrated using Trivy to check for vulnerabilities in Docker images.