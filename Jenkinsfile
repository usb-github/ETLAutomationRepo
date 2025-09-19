pipeline {
    agent any
    
    environment {
        // Database configuration
        DB_SERVER = "DESKTOP-77LK4FJ"  // Your server name
        DB_NAME = "northwind"          // Your database name
    }
    
    stages {
        stage('Setup Credentials') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'sql-server-credentials',
                        usernameVariable: 'DB_USER',
                        passwordVariable: 'DB_PASSWORD'
                    )]) {
                        // Make credentials available to subsequent stages
                        env.DB_USER = "$DB_USER"
                        env.DB_PASSWORD = "$DB_PASSWORD"
                    }
                }
            }
        }
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Run Tests') {
            steps {
                // Run the tests with pytest
                bat '''
                    python -m pytest test_ETL_data_core.py --html=report.html --self-contained-html
                '''
            }
        }
        
        stage('Publish Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'report.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }
}