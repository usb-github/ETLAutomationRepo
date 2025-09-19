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
                withCredentials([usernamePassword(
                    credentialsId: 'sql-server-credentials',
                    usernameVariable: 'DB_USER',
                    passwordVariable: 'DB_PASSWORD'
                )]) {
                    bat '''
                        set DB_USER=%DB_USER%
                        set DB_PASSWORD=%DB_PASSWORD%
                        set DB_SERVER=DESKTOP-77LK4FJ
                        set DB_NAME=northwind
                    '''
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
                withCredentials([usernamePassword(
                    credentialsId: 'sql-server-credentials',
                    usernameVariable: 'DB_USER',
                    passwordVariable: 'DB_PASSWORD'
                )]) {
                    bat '''
                        echo Using DB_USER: %DB_USER%
                        echo Using DB_SERVER: %DB_SERVER%
                        echo Using DB_NAME: %DB_NAME%
                        python -m pytest test_ETL_data_core.py --html=report.html --self-contained-html
                    '''
                }
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