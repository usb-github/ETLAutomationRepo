pipeline {
    agent any
    
    environment {
        PYTHON_PATH = 'C:\\Python313\\python.exe'
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
                    bat """
                        ${PYTHON_PATH} -m pip install --upgrade pip
                        ${PYTHON_PATH} -m pip install pytest pytest-html pandas numpy
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
    }
}
