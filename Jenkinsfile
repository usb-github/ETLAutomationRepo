pipeline {
    agent any
    
    environment {
        // Database configuration
        DB_SERVER = "DESKTOP-77LK4FJ"  // Your server name
        DB_NAME = "northwind"          // Your database name
    }
    
    stages {
        stage('Test DB Connection') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'sql-server-credentials', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASSWORD')]) {
                    script {
                        // Create a temporary Python script with proper credentials
                        writeFile file: 'test_connection.py', text: """
import pyodbc
print('Testing connection...')
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=${DB_SERVER};DATABASE=${DB_NAME};UID={env.DB_USER};PWD={env.DB_PASSWORD};Encrypt=yes;TrustServerCertificate=yes;'
conn = pyodbc.connect(conn_str)
print('Connection successful!')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM [order_details]')
print(f'Number of records in order_details: {cursor.fetchone()[0]}')
conn.close()
"""
                        // Execute the Python script
                        bat 'python test_connection.py'
                        // Clean up the temporary file
                        bat 'del test_connection.py'
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
                withCredentials([usernamePassword(credentialsId: 'sql-server-credentials', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASSWORD')]) {
                    bat '''
                        set DB_USER=%DB_USER%
                        set DB_PASSWORD=%DB_PASSWORD%
                        python -m pytest test_ETL_data_core.py --html=report.html --self-contained-html -v
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