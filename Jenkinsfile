pipeline {
    agent any

    environment {
        SONARQUBE_TOKEN = credentials('sonarqube-token-id') // Токен SonarQube
    }

    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main', url: 'https://github.com/agarkovv/example-sentiment-project'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t sentiment-app .'
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    sh 'pytest --alluredir=allure-results'
                }
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner -Dsonar.projectKey=sentiment-analysis -Dsonar.sources=. -Dsonar.host.url=$SONAR_HOST_URL -Dsonar.login=$SONARQUBE_TOKEN'
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh './build.sh'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
