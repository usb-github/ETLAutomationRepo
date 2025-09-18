pipeline {
    agent any
    
    triggers {
        pollSCM('H/5 * * * *')  // Poll every 5 minutes for changes
    }
    
    environment {
        // Python and path settings
        PYTHON_PATH = 'C:\\Python313\\python.exe'
        ETL_TEST_DATA = 'D:/ETL Testing - Python'
        
        // Database connection settings (adjust these in Jenkins credentials)
        DB_SERVER = 'DESKTOP-77LK4FJ'
        DB_NAME = 'northwind'
        DB_DRIVER = '{ODBC Driver 17 for SQL Server}'
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Checkout code from your GitHub repository
                git branch: 'master',
                    url: 'https://github.com/usb-github/ETLAutomationRepo.git'
            }
        }
        
        stage('Setup Python Environment') {
            steps {
                script {
                    // Create test data directory if it doesn't exist
                    bat "if not exist \"${ETL_TEST_DATA}\" mkdir \"${ETL_TEST_DATA}\""
                    
                    // Install required Python packages including pyodbc
                    bat """
                        ${PYTHON_PATH} -m pip install --upgrade pip
                        ${PYTHON_PATH} -m pip install pytest pytest-html pandas numpy pyodbc
                    """
                }
            }
        }
        
        stage('Verify Database Connection') {
            steps {
                script {
                    // Create a simple Python script to test the database connection
                    writeFile file: 'test_connection.py', text: """
import pyodbc
conn_str = (
    "DRIVER=${DB_DRIVER};"
    "SERVER=${DB_SERVER};"
    "DATABASE=${DB_NAME};"
    "Trusted_Connection=yes;"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)
try:
    conn = pyodbc.connect(conn_str)
    print("Database connection successful!")
    conn.close()
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit(1)
"""
                    // Test the connection
                    bat "${PYTHON_PATH} test_connection.py"
                }
            }
        }
        
        stage('Prepare Test Data') {
            steps {
                script {
                    // Copy test data files if they exist in the repository
                    bat """
                        if exist "ETL pipeline test\\duplicatecheck.csv" copy "ETL pipeline test\\duplicatecheck.csv" "${ETL_TEST_DATA}\\"
                        if exist "ETL pipeline test\\order_details.csv" copy "ETL pipeline test\\order_details.csv" "${ETL_TEST_DATA}\\"
                    """
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    bat """
                        cd "ETL pipeline test"
                        ${PYTHON_PATH} -m pytest test_ETL_data_core.py -v --html="ETL_data_core_Test_Results.html" --self-contained-html
                    """
                }
            }
        }
    }
    
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'ETL pipeline test',
                reportFiles: 'ETL_data_core_Test_Results.html',
                reportName: 'ETL Test Report',
                reportTitles: 'ETL Test Results'
            ])
            
            archiveArtifacts artifacts: 'ETL pipeline test/ETL_data_core_Test_Results.html', fingerprint: true
        }
        failure {
            echo 'Test execution failed! Check the HTML report for details.'
        }
        cleanup {
            // Clean up temporary files
            bat "del test_connection.py"
        }
    }
}
