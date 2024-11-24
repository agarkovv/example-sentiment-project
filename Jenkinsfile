pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = '/usr/local/bin/docker-compose'
        SONARQUBE = 'SonarQube'
        SONARQUBE_TOKEN = credentials('sonarqube-token')
        ALLURE_RESULTS = "allure-results"
        TEST_REPORTS = "target/test-*.xml"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/agarkovv/example-sentiment-project'
            }
        }

        stage('Build Application') {
            steps {
                script {
                    sh "docker-compose -f docker-compose.yml build"
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    sh "pytest --maxfail=1 --disable-warnings -q"
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    // Run the SonarQube analysis using Maven (or Python-based tools if applicable)
                    withSonarQubeEnv('SonarQube') {
                        sh 'mvn sonar:sonar' // If using Maven for analysis, otherwise adjust to Python-based tools
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                script {
                    // Generate Allure report from pytest results
                    sh "allure serve ${ALLURE_RESULTS}"
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    // Use Docker Compose to deploy the application
                    sh "docker-compose -f docker-compose.yml up -d"
                }
            }
        }
    }

    post {
        always {
            junit "**/target/test-*.xml"
            allure()
        }
        success {
            echo 'Build, test, and deploy succeeded!'
        }
        failure {
            echo 'Something went wrong during the pipeline.'
        }
    }
}