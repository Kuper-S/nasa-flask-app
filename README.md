NASA Flask App Deployment on Kubernetes
This documentation outlines the steps taken to deploy a NASA Flask application on Kubernetes, including MongoDB and Kafka integration, user management, and setting up ingress for external access.

Prerequisites
Kubernetes cluster (Minikube or any other cluster)
Helm installed and configured
Docker installed for building and pushing images
MongoDB and Kafka running in the cluster
Ingress controller (such as Nginx) installed in the cluster
Admin access to MongoDB and Kafka
Table of Contents
Setting Up the Application
MongoDB Configuration
Kafka Configuration
Deploying the Application Using Helm
Ingress Configuration
Creating MongoDB Users
Accessing the Application
1. Setting Up the Application
The NASA Flask app is built and deployed using Docker and Helm. Here's a step-by-step guide:

Build the Docker Image:

Navigate to the root directory of your application:
bash
Copy code
docker build -t kupidun/nasa-flask-app:1.0.3 .
Push the Image to Docker Hub:

Push the image to a Docker registry (ensure you are logged in):
bash
Copy code
docker push kupidun/nasa-flask-app:1.0.3
2. MongoDB Configuration
2.1 Deploy MongoDB in the Cluster
You can deploy MongoDB using a Helm chart or manually. Below is an example of deploying MongoDB with Kubernetes:

bash
Copy code
kubectl apply -f mongodb-deployment.yaml
Ensure that MongoDB is running:

bash
Copy code
kubectl get pods -n db
2.2 Accessing MongoDB Inside the Cluster
Connect to MongoDB Pod:

bash
Copy code
kubectl exec -it mongodb-<pod-name> -n db -- mongosh --username root --password <admin-password> --authenticationDatabase admin
Create Database and Collections:

Inside the MongoDB shell, you can switch to a database and create collections.

javascript
Copy code
use nasa_db
3. Kafka Configuration
3.1 Kafka Plain Text Configuration
Kafka has been configured with plain text authentication for simplicity. The relevant changes were made in the server.properties file:

properties
Copy code
listener.security.protocol.map=CLIENT:PLAINTEXT,INTERNAL:PLAINTEXT,CONTROLLER:PLAINTEXT
sasl.enabled.mechanisms=PLAIN
listener.name.client.plain.sasl.jaas.config=org.apache.kafka.common.security.plain.PlainLoginModule required user_user1="password";
3.2 Kafka Deployment
If Kafka is not yet deployed, follow these steps to deploy Kafka:

bash
Copy code
helm install kafka bitnami/kafka --namespace messaging
Check if Kafka is running:

bash
Copy code
kubectl get pods -n messaging
4. Deploying the Application Using Helm
4.1 Helm Chart Setup
The Helm chart nasa-flask-app was used to deploy the Flask application. The values.yaml contains configurations for the image, environment variables, and Kubernetes resources.

yaml
Copy code
env:
  - name: MONGO_USER
    valueFrom:
      secretKeyRef:
        name: mongodb-secret
        key: mongo-username
  - name: MONGO_PASSWORD
    valueFrom:
      secretKeyRef:
        name: mongodb-secret
        key: mongo-password
  - name: MONGO_URI
    value: "mongodb://$(MONGO_USER):$(MONGO_PASSWORD)@mongodb.db.svc.cluster.local:27017/nasa_db"
  - name: KAFKA_BOOTSTRAP_SERVERS
    value: "kafka.messaging.svc.cluster.local:9092"
  - name: KAFKA_SASL_USERNAME
    valueFrom:
      secretKeyRef:
        name: kafka-secret
        key: kafka-username
  - name: KAFKA_SASL_PASSWORD
    valueFrom:
      secretKeyRef:
        name: kafka-secret
        key: kafka-password
4.2 Helm Install or Upgrade
To install or upgrade the application using Helm:

bash
Copy code
helm upgrade --install nasa-flask-app ./helm-chart -n app
5. Ingress Configuration
Ingress was used to expose the application externally. Below is an example of an ingress resource:

yaml
Copy code
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nasa-flask-ingress
  namespace: app
spec:
  rules:
    - host: nasa-app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: nasa-flask-app
                port:
                  number: 5000
Apply the ingress resource:

bash
Copy code
kubectl apply -f ingress.yaml
Verify the ingress URL:

bash
Copy code
kubectl get ingress -n app
Ensure the ingress controller is set up correctly and DNS or /etc/hosts is updated to point to nasa-app.example.com.

6. Creating MongoDB Users
6.1 Create a MongoDB User Script
To automate MongoDB user creation, a script was written to create a new user. Here’s how to run the script:

Script Creation:

Create a script named create-mongo-user.sh:

bash
Copy code
#!/bin/bash
read -p "Enter MongoDB Username: " MONGO_USER
read -sp "Enter MongoDB Password: " MONGO_PASSWORD
echo
read -p "Enter MongoDB Database: " MONGO_DB

mongosh --username root --password <admin-password> --authenticationDatabase admin <<EOF
use $MONGO_DB
db.createUser({
  user: "$MONGO_USER",
  pwd: "$MONGO_PASSWORD",
  roles: [ { role: "readWrite", db: "$MONGO_DB" } ]
})
EOF

echo "User $MONGO_USER created successfully for database $MONGO_DB."
Run the Script:

bash
Copy code
chmod +x create-mongo-user.sh
./create-mongo-user.sh
This script will prompt you for a username, password, and database name and create the user in the MongoDB database.

7. Accessing the Application
After the app is deployed and ingress is configured, the app can be accessed via the ingress URL:

bash
Copy code
http://nasa-app.example.com
Make sure that DNS is set up, or if you are using Minikube, you may need to add the IP of the Minikube node to your /etc/hosts file.

Example:

bash
Copy code
192.168.49.2 nasa-app.example.com
Troubleshooting
1. Check Pod Logs:
bash
Copy code
kubectl logs <pod-name> -n app
2. Check Kafka Logs:
bash
Copy code
kubectl logs <kafka-pod-name> -n messaging
3. MongoDB Authentication Issues:
Make sure MongoDB users are created in the correct database, and credentials are correct.

This documentation should provide a complete step-by-step guide for setting up and deploying the NASA Flask App in Kubernetes with MongoDB, Kafka, and ingress. You can add more details as needed for your specific environment!
