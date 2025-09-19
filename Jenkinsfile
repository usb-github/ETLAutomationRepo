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
                    bat '''
                        echo import pyodbc > test_connection.py
                        echo print('Testing connection...') >> test_connection.py
                        echo conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=%DB_SERVER%;DATABASE=%DB_NAME%;UID=%%DB_USER%%;PWD=%%DB_PASSWORD%%;Encrypt=yes;TrustServerCertificate=yes;" >> test_connection.py
                        echo conn = pyodbc.connect(conn_str) >> test_connection.py
                        echo print('Connection successful!') >> test_connection.py
                        echo cursor = conn.cursor() >> test_connection.py
                        echo cursor.execute('SELECT COUNT(*) FROM [order_details]') >> test_connection.py
                        echo print(f'Number of records in order_details: {cursor.fetchone()[0]}') >> test_connection.py
                        echo conn.close() >> test_connection.py
                        python test_connection.py
                        del test_connection.py
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
                withCredentials([usernamePassword(credentialsId: 'sql-server-credentials', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASSWORD')]) {
                    bat '''
                        set DB_USER=%DB_USER%
                        set DB_PASSWORD=%DB_PASSWORD%
                        set DB_SERVER=%DB_SERVER%
                        set DB_NAME=%DB_NAME%
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