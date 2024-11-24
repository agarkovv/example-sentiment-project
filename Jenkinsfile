pipeline {
    agent any

    environment {
        SONARQUBE_TOKEN = credentials('sonarqube-token')
        DOCKER_IMAGE = 'python:3.11'
    }

    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main', url: 'https://github.com/agarkovv/example-sentiment-project'
            }
        }

        // stage('Build Docker Image') {
        //     steps {
        //         script {
        //             sh 'docker build -t sentiment-app .'
        //         }
        //     }
        // }

        stage('Debug') {
            steps {
                script {
                    sh 'pwd'
                    sh 'ls -la'
                }
            }
        }

        stage('Run Unit Tests in Docker') {
            steps {
                script {
                    echo 'Running Unit Tests inside Docker...'
                    sh '''
                    docker run --rm -v $(pwd):/workspace -w /workspace python:3.11 /bin/bash -c "
                        # Ensure all necessary files are in place
                        cp -r /workspace /tmp/workdir &&
                        cd /tmp/workdir &&
                        ls -la &&

                        # Setup virtual environment
                        python3 -m venv .venv &&
                        . .venv/bin/activate &&

                        # Install dependencies and run tests
                        pip install --upgrade pip &&
                        pip install -r requirements.txt &&
                        pytest --alluredir=allure-results tests/
                    "
                    '''
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
                    sh '''
                    sonar-scanner \
                        -Dsonar.projectKey=sentiment-analysis \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=$SONAR_HOST_URL \
                        -Dsonar.login=$SONARQUBE_TOKEN
                    '''
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
