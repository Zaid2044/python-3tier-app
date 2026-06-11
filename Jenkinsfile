pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"

        ACCOUNT_ID = "234273295663"

        BACKEND_REPO = "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/python-backend"
        FRONTEND_REPO = "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/python-frontend"

        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Docker Login') {
            steps {
                sh '''
                aws ecr get-login-password --region ${AWS_REGION} \
                | docker login \
                --username AWS \
                --password-stdin ${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
                '''
            }
        }

        stage('Build Backend Image') {
            steps {
                sh '''
                docker build \
                -t python-backend:${IMAGE_TAG} \
                ./backend
                '''
            }
        }

        stage('Tag Backend Image') {
            steps {
                sh '''
                docker tag python-backend:${IMAGE_TAG} \
                ${BACKEND_REPO}:${IMAGE_TAG}
                '''
            }
        }

        stage('Push Backend Image') {
            steps {
                sh '''
                docker push ${BACKEND_REPO}:${IMAGE_TAG}
                '''
            }
        }

        stage('Build Frontend Image') {
            steps {
                sh '''
                docker build \
                -t python-frontend:${IMAGE_TAG} \
                ./frontend
                '''
            }
        }

        stage('Tag Frontend Image') {
            steps {
                sh '''
                docker tag python-frontend:${IMAGE_TAG} \
                ${FRONTEND_REPO}:${IMAGE_TAG}
                '''
            }
        }

        stage('Push Frontend Image') {
            steps {
                sh '''
                docker push ${FRONTEND_REPO}:${IMAGE_TAG}
                '''
            }
        }
    }

    post {
        always {
            sh '''
            docker image prune -af || true
            '''
        }
    }
}