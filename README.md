<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NASA Flask App CI/CD Pipeline</title>
</head>
<body>

  <h1>NASA Flask App CI/CD Pipeline</h1>

  <h2>Introduction</h2>
  <p>The NASA Flask App is a web application built using the Flask framework to fetch and display data from NASA's public APIs. This app is containerized using Docker and designed for deployment in a Kubernetes environment with integrated scaling, service discovery, and network policies. It also supports continuous integration and continuous deployment (CI/CD) with tools such as Jenkins, SonarQube, and ArgoCD.</p>

  <h2>Features</h2>
  <ul>
    <li>API Integration: Fetches data from NASA's public APIs.</li>
    <li>Flask Web Framework: Lightweight and simple web server.</li>
    <li>Gunicorn for Production: Used as a WSGI HTTP Server for Flask in production.</li>
    <li>Dockerized: Built as a Docker image for portability and scalability.</li>
    <li>Kubernetes-Ready: Contains manifests for Kubernetes deployment, auto-scaling, and service discovery.</li>
    <li>CI/CD: Integrated with Jenkins and ArgoCD for automated testing and deployment.</li>
    <li>Horizontal Pod Autoscaler (HPA): Automatically scales the app based on CPU utilization.</li>
  </ul>

  <h2>Prerequisites</h2>
  <ul>
    <li>Kubernetes Cluster: A running Kubernetes cluster (e.g., Minikube, EKS, or GKE).</li>
    <li>Docker: Installed locally for containerization.</li>
    <li>kubectl: CLI for interacting with Kubernetes.</li>
    <li>Helm: For managing Kubernetes applications.</li>
    <li>Metrics Server: For HPA functionality in Kubernetes.</li>
    <li>GitHub Account: For CI/CD pipelines and GitOps with ArgoCD.</li>
    <li>ArgoCD: Installed and configured for continuous deployment.</li>
    <li>SonarQube: For static code analysis (optional but recommended).</li>
    <li>AWS CLI: Configured if deploying on AWS.</li>
    <li>Terraform: Installed for infrastructure provisioning.</li>
  </ul>

  <h2>Project Structure</h2>
  <pre>
    ├── app/                  # Application source code
    ├── Dockerfile             # Dockerfile for building the image
    ├── helm/                  # Helm charts for Kubernetes deployment
    ├── .circleci/             # CircleCI pipeline configuration
    ├── .github/workflows/     # GitHub Actions workflows
    ├── requirements.txt       # Python dependencies
    └── README.md              # Project documentation
  </pre>

  <h2>Setup Instructions</h2>

  <h3>1. Clone the Repository</h3>
  <pre>
    git clone https://github.com/your-username/nasa-flask-app.git
    cd nasa-flask-app
  </pre>

  <h3>2. Install Dependencies</h3>
  <pre>
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
  </pre>

  <h3>3. Build Docker Image</h3>
  <pre>
    docker build -t nasa-flask-app:latest .
  </pre>

  <h3>4. Run Locally with Docker</h3>
  <pre>
    docker run -p 5000:5000 nasa-flask-app:latest
  </pre>

  <h2>CI/CD Integration</h2>
  <p>CircleCI configuration is defined in `.circleci/config.yml` with jobs for building Docker images, running tests, and deploying the application.</p>

  <h2>Kubernetes Deployment</h2>

  <h3>Deploy with Helm</h3>
  <pre>
    helm install nasa-flask-app ./helm
  </pre>

  <h3>Verify the Deployment</h3>
  <pre>
    kubectl get pods
  </pre>

  <h2>Static Code Analysis</h2>
  <p>SonarQube is integrated for static code analysis. Install it using Helm and access the dashboard via port-forwarding.</p>

  <h2>Contributing</h2>
  <p>To contribute, fork the repository, create a new branch, commit changes, and submit a pull request.</p>

  <h2>License</h2>
  <p>This project is licensed under the MITSure! Here's the README file formatted in **HTML**:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NASA Flask App CI/CD Pipeline</title>
</head>
<body>
    <h1>NASA Flask App CI/CD Pipeline</h1>

    <h2>Introduction</h2>
    <p>
        The NASA Flask App is a web application built using the Flask framework to fetch and display data from NASA's public APIs. 
        This app is containerized using Docker and designed for deployment in a Kubernetes environment with integrated scaling, service discovery, 
        and network policies. It also supports continuous integration and continuous deployment (CI/CD) with tools such as Jenkins, SonarQube, and ArgoCD.
    </p>

    <h2>Features</h2>
    <ul>
        <li>API Integration: Fetches data from NASA's public APIs.</li>
        <li>Flask Web Framework: Lightweight and simple web server.</li>
        <li>Gunicorn for Production: Used as a WSGI HTTP Server for Flask in production.</li>
        <li>Dockerized: Built as a Docker image for portability and scalability.</li>
        <li>Kubernetes-Ready: Contains manifests for Kubernetes deployment, auto-scaling, and service discovery.</li>
        <li>CI/CD: Integrated with Jenkins and ArgoCD for automated testing and deployment.</li>
        <li>Horizontal Pod Autoscaler (HPA): Automatically scales the app based on CPU utilization.</li>
    </ul>

    <h2>Prerequisites</h2>
    <ul>
        <li>Kubernetes Cluster: A running Kubernetes cluster (e.g., Minikube, EKS, or GKE).</li>
        <li>Docker: Installed locally for containerization.</li>
        <li>kubectl: CLI for interacting with Kubernetes.</li>
        <li>Helm: For managing Kubernetes applications.</li>
        <li>Metrics Server: For HPA functionality in Kubernetes.</li>
        <li>GitHub Account: For CI/CD pipelines and GitOps with ArgoCD.</li>
        <li>SonarQube: For static code analysis (optional but recommended).</li>
        <li>AWS CLI: Configured if deploying on AWS.</li>
        <li>Terraform: Installed for infrastructure provisioning.</li>
    </ul>

    <h2>Project Structure</h2>
    <pre>
        ├── app/                  # Application source code
        ├── Dockerfile             # Dockerfile for building the image
        ├── helm/                  # Helm charts for Kubernetes deployment
        ├── .circleci/             # CircleCI pipeline configuration
        ├── .github/workflows/     # GitHub Actions workflows
        ├── requirements.txt       # Python dependencies
        └── README.md              # Project documentation
    </pre>

    <h2>Setup Instructions</h2>

    <h3>1. Clone the Repository</h3>
    <pre>
    git clone https://github.com/your-username/nasa-flask-app.git
    cd nasa-flask-app
    </pre>

    <h3>2. Install Dependencies</h3>
    <pre>
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    </pre>

    <h3>3. Build Docker Image</h3>
    <pre>
    docker build -t nasa-flask-app:latest .
    </pre>

    <h3>4. Run Locally with Docker</h3>
    <pre>
    docker run -p 5000:5000 nasa-flask-app:latest
    </pre>

    <h2>CI/CD Integration</h2>
    <p>CircleCI configuration is defined in `.circleci/config.yml` with jobs for building Docker images, running tests, and deploying the application.</p>

    <h2>Kubernetes Deployment</h2>

    <h3>Deploy with Helm</h3>
    <pre>
    helm install nasa-flask-app ./helm
    </pre>

    <h3>Verify the Deployment</h3>
    <pre>
    kubectl get pods
    </pre>

    <h2>Static Code Analysis</h2>
    <p>SonarQube is integrated for static code analysis. Install it using Helm and access the dashboard via port-forwarding.</p>

    <h2>Contributing</h2>
    <p>To contribute, fork the repository, create a new branch, commit changes, and submit a pull request.</p>

    <h2>License</h2>
    <p>This project is licensed under the MIT License.</p>
</body>
</html>
