// Jenkinsfile
// This file defines the Continuous Integration/Continuous Delivery pipeline.

// The 'pipeline' block is the root block for a Declarative Pipeline.
pipeline {
    // Define the agent where the pipeline will run.
    // 'any' means Jenkins will run the pipeline on any available agent.
    agent any

    // Define environment variables for the virtual environment path
    environment {
        // Define the path for the virtual environment.
        // It's good practice to place it within the workspace.
        VENV_PATH = "${WORKSPACE}/venv"
        // Add /usr/local/bin to PATH to ensure minikube and kubectl are found
        PATH = "/usr/local/bin:${env.PATH}"
    }

    // The 'stages' block defines the different phases of your pipeline.
    stages {
        // Stage 1: Checkout - Get the latest code from the Git repository.
        stage('Checkout') {
            steps {
                script {
                    echo 'Checking out source code...'
                    checkout scm
                }
            }
        }

        // Stage 2: Setup Environment & Build - Create virtual environment and install dependencies.
        stage('Setup Environment & Build') {
            steps {
                script {
                    echo 'Creating Python virtual environment and installing dependencies...'
                    // Create a virtual environment
                    sh 'python3 -m venv "${VENV_PATH}"'
                    // Activate the virtual environment and then install dependencies.
                    // We explicitly use 'bash -c' to ensure the 'source' command is available.
                    sh 'bash -c "source \\"${VENV_PATH}/bin/activate\\" && pip install -r requirements.txt"'
                }
            }
        }

        // Stage 3: Test - Run unit tests for the Python application within the virtual environment.
        stage('Test') {
            steps {
                script {
                    echo 'Running unit tests...'
                    // Activate the virtual environment and then run tests.
                    // We explicitly use 'bash -c' to ensure the 'source' command is available.
                    sh 'bash -c "source \\"${VENV_PATH}/bin/activate\\" && python3 -m unittest test_app.py"'
                }
            }
        }

        // Stage 4: Build Docker Image - Create a Docker image of the application.
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Checking Minikube status and setting Docker environment...'
                    // Check if Minikube is running. If not, this step will fail.
                    sh 'minikube status'

                    // Set the Docker environment to point to Minikube's Docker daemon.
                    // We use 'eval $(minikube docker-env)' to set environment variables.
                    // The 'set -xe' ensures that the script exits immediately if any command fails.
                    // We also capture the output of minikube docker-env to ensure it's valid.
                    sh '''
                        set -xe
                        eval "$(minikube docker-env)"
                    '''

                    echo 'Building Docker image...'
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
