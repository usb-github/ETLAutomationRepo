pipeline {
    agent any
    
    environment {
        // Database configuration for Windows Authentication
        DB_SERVER = "DESKTOP-77LK4FJ"  // Your server name
        DB_NAME = "northwind"          // Your database name
    }
    
    stages {
        stage('Test DB Connection') {
            steps {
                script {
                    def connectionTest = """
import pyodbc

print('Testing connection...')
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-77LK4FJ;"
    "DATABASE=northwind;"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

conn = pyodbc.connect(conn_str)
print('Connection successful!')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM [order_details]')
print(f'Number of records in order_details: {cursor.fetchone()[0]}')
conn.close()
"""
                    writeFile file: 'test_connection.py', text: connectionTest
                    bat 'python test_connection.py'
                    bat 'del test_connection.py'
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
                script {
                    bat 'python -m pytest test_ETL_data_core.py --html=report.html --self-contained-html -v'
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
    
    post {
        always {
            cleanWs()
        }
    }
}