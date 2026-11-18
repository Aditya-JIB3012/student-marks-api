pipeline {
    agent any

    environment {
        IMAGE_NAME  = "student-marks-api"
        IMAGE_TAG   = "${env.GIT_COMMIT?.take(7) ?: env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                echo "Building commit: ${IMAGE_TAG}"
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        // CI Enhancement: Automated tests run BEFORE the build
        stage('Test') {
            steps {
                sh 'pytest tests/ -v --tb=short'
            }
            post {
                always {
                    echo 'Test stage complete.'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                // CI Enhancement: image tagged with Git commit SHA (first 7 chars)
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag  ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
                echo "Docker image built and tagged as ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Archive Build Info') {
            steps {
                // Archive a build-info file (acts as the "build artifact" record)
                sh """
                    echo "Build: ${IMAGE_TAG}" > build-info.txt
                    echo "Commit: ${env.GIT_COMMIT}" >> build-info.txt
                    echo "Timestamp: \$(date)" >> build-info.txt
                """
                archiveArtifacts artifacts: 'build-info.txt', fingerprint: true
            }
        }
    }

    post {
        success { echo 'Pipeline succeeded!' }
        failure { echo 'Pipeline failed — check the logs above.' }
    }
}
