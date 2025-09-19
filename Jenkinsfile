pipeline {
    agent any
    
    environment {
        // Using credentials binding
        SQL_CREDS = credentials('sql-server-credentials')
        DB_USER = "${SQL_CREDS_USR}"
        DB_PASSWORD = "${SQL_CREDS_PSW}"
        DB_SERVER = "DESKTOP-77LK4FJ"  // Your server name
        DB_NAME = "northwind"          // Your database name
    }
    
    stages {
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