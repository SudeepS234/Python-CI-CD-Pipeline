// Jenkinsfile
// This file defines the Continuous Integration/Continuous Delivery pipeline.

// The 'pipeline' block is the root block for a Declarative Pipeline.
pipeline {
    // Define the agent where the pipeline will run.
    // 'any' means Jenkins will run the pipeline on any available agent.
    agent any

    // Define tools required for the pipeline.
    // We specify a Python 3.9 installation. Ensure this is configured in Jenkins
    // (Manage Jenkins -> Global Tool Configuration -> JDK and Python installations).
    // If you don't have a specific Python installation configured in Jenkins,
    // you might need to rely on the system's default Python or install it within the agent.
    // For Dockerized Jenkins, you might need to ensure Python is installed inside the Jenkins container,
    // or use a custom Jenkins agent image with Python pre-installed.
    // For simplicity, we'll execute shell commands assuming Python is available.
    // If your Jenkins container doesn't have Python, you might need to modify the Dockerfile for Jenkins
    // or use a Jenkins agent with Python.
    // For this basic setup, we'll assume the 'python3' command is available globally.

    // The 'stages' block defines the different phases of your pipeline.
    stages {
        // Stage 1: Checkout - Get the latest code from the Git repository.
        stage('Checkout') {
            steps {
                // 'checkout scm' checks out the code from the SCM (Source Code Management)
                // configured in the Jenkins job (which is our GitHub repository).
                script {
                    echo 'Checking out source code...'
                    checkout scm
                }
            }
        }

        // Stage 2: Build - Install Python dependencies.
        stage('Build') {
            steps {
                script {
                    echo 'Installing Python dependencies...'
                    // Execute shell command to install dependencies from requirements.txt.
                    // We use 'pip' directly here, assuming it's in the PATH.
                    // If you have multiple Python versions, you might need 'pip3'.
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        // Stage 3: Test - Run unit tests for the Python application.
        stage('Test') {
            steps {
                script {
                    echo 'Running unit tests...'
                    // Execute shell command to run Python unit tests.
                    // '-m unittest' runs the unittest module.
                    sh 'python3 -m unittest test_app.py'
                }
            }
        }

        // Stage 4: Build Docker Image - Create a Docker image of the application.
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image...'
                    // This command is crucial for Minikube. It configures the shell
                    // to use Minikube's Docker daemon. This means any 'docker' commands
                    // executed afterwards will build images directly into Minikube's
                    // internal Docker registry, making them available to Kubernetes.
                    sh 'eval $(minikube docker-env)'

                    // Build the Docker image.
                    // '-t python-ci-cd-app:latest' tags the image with a name and 'latest' tag.
                    // '.' indicates that the Dockerfile is in the current directory.
                    sh 'docker build -t python-ci-cd-app:latest .'
                }
            }
        }

        // Stage 5: Deploy to Kubernetes - Apply Kubernetes deployment and service configurations.
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo 'Deploying to Kubernetes...'
                    // Apply the Kubernetes deployment configuration.
                    // This creates or updates the Deployment object in Kubernetes.
                    sh 'kubectl apply -f deployment.yaml'

                    // Apply the Kubernetes service configuration.
                    // This creates or updates the Service object, exposing your application.
                    sh 'kubectl apply -f service.yaml'

                    echo 'Deployment to Kubernetes complete.'
                }
            }
        }
    }

    // The 'post' section defines actions to take after the pipeline completes,
    // regardless of success or failure.
    post {
        // Always block ensures this runs after every build.
        always {
            // Clean up workspace after the build.
            // This is good practice to free up disk space.
            script {
                echo 'Cleaning up workspace...'
                cleanWs()
            }
        }
        // You can add more post-build actions here, e.g., sending notifications.
        // success {
        //     echo 'Pipeline succeeded!'
        // }
        // failure {
        //     echo 'Pipeline failed!'
        // }
    }
}
