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
                        def connectionTest = """
import os
import pyodbc

print('Testing connection...')
os.environ['DB_USER'] = '${DB_USER}'
os.environ['DB_PASSWORD'] = '${DB_PASSWORD}'
os.environ['DB_SERVER'] = '${DB_SERVER}'
os.environ['DB_NAME'] = '${DB_NAME}'

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={os.environ['DB_SERVER']};"
    f"DATABASE={os.environ['DB_NAME']};"
    f"UID={os.environ['DB_USER']};"
    f"PWD={os.environ['DB_PASSWORD']};"
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
        }
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Run Tests') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'sql-server-credentials', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASSWORD')]) {
                    script {
                        // Create a wrapper script to set environment variables
                        def testWrapper = '''
import os
import subprocess

# Set environment variables
os.environ['DB_USER'] = '${DB_USER}'
os.environ['DB_PASSWORD'] = '${DB_PASSWORD}'
os.environ['DB_SERVER'] = '${DB_SERVER}'
os.environ['DB_NAME'] = '${DB_NAME}'

# Run pytest with the environment variables set
result = subprocess.run(['python', '-m', 'pytest', 'test_ETL_data_core.py', '--html=report.html', '--self-contained-html', '-v'])
exit(result.returncode)
'''
                        writeFile file: 'run_tests.py', text: testWrapper
                        bat 'python run_tests.py'
                        bat 'del run_tests.py'
                    }
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