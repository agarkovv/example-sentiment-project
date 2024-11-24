pipeline {
    agent any

    environment {
        // DOCKER_COMPOSE = '/usr/local/bin/docker-compose'
        SONARQUBE = 'SonarQube'
        SONARQUBE_TOKEN = credentials('sonarqube-token')
        ALLURE_RESULTS = "allure-results"
        TEST_REPORTS = "target/test-*.xml"
    }

    stages {
        stage('Clone repository') {
            steps {
                git branch: 'main', url: 'https://github.com/agarkovv/example-sentiment-project'
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
                    sh "docker-compose -f docker-compose.test.yml up -d"
                    sh "docker-compose -f docker-compose.test.yml down"
                }
            }
        }

        // stage('SonarQube Analysis') {
        //     steps {
        //         script {
        //             withSonarQubeEnv('SonarQube') {
        //                 sh 'mvn sonar:sonar'
        //             }
        //         }
        //     }
        // }

        stage('Generate Allure Report') {
            steps {
                script {
                    sh "allure serve ${ALLURE_RESULTS}"
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    sh "docker-compose -f docker-compose.yml up -d"
                }
            }
        }
    }

    post {
        always {
            junit '**/target/test-*.xml'
            allure results: ['**/allure-results']
        }
        success {
            echo 'Build, test, and deploy succeeded!'
        }
        failure {
            echo 'Something went wrong during the pipeline.'
        }
    }


}