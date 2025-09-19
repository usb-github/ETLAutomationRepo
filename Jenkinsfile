pipeline {
    agent any
    
    environment {
        // Database configuration
        DB_SERVER = "DESKTOP-77LK4FJ"  // Your server name
        DB_NAME = "northwind"          // Your database name
        // Bind credentials to environment variables
        MSSQL_CREDS = credentials('sql-server-credentials')
        DB_USER = "${MSSQL_CREDS_USR}"
        DB_PASSWORD = "${MSSQL_CREDS_PSW}"
    }
    
    stages {
        stage('Verify Environment') {
            steps {
                bat '''
                    echo Testing environment variables:
                    echo DB_SERVER: %DB_SERVER%
                    echo DB_NAME: %DB_NAME%
                    echo DB_USER: %DB_USER%
                '''
            }
        }
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Run Tests') {
            steps {
                bat '''
                    python -m pytest test_ETL_data_core.py --html=report.html --self-contained-html -v
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