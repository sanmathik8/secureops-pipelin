pipeline {
    agent any
    environment {
        GITHUB_TOKEN = credentials('github-token')
        GITHUB_REPO  = 'sanmathik8/secureops-pipeline'
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/sanmathik8/secureops-pipeline.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t secureops-app:latest .'
            }
        }
        stage('Security Scan') {
            steps {
                sh '''
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy image \
                        --exit-code 0 \
                        --severity HIGH,CRITICAL \
                        --format json \
                        -o trivy-report.json \
                        secureops-app:latest
                '''
            }
        }
        stage('Check Critical Vulnerabilities') {
            steps {
                sh '''
                    python3 -c "
import json, sys
with open('trivy-report.json') as f:
    data = json.load(f)
critical = sum(
    1 for r in data.get('Results', [])
    for v in r.get('Vulnerabilities', [])
    if v.get('Severity') == 'CRITICAL'
)
print(f'CRITICAL vulnerabilities found: {critical}')
sys.exit(1 if critical > 0 else 0)
"
                '''
            }
        }
        stage('Auto Fix Vulnerable Packages') {
            when {
                expression {
                    def result = sh(script: '''
                        python3 -c "
import json
with open('trivy-report.json') as f:
    data = json.load(f)
critical = sum(
    1 for r in data.get('Results', [])
    for v in r.get('Vulnerabilities', [])
    if v.get('Severity') == 'CRITICAL'
)
print(critical)
"
                    ''', returnStdout: true).trim()
                    return result.toInteger() > 0
                }
            }
            steps {
                sh '''
                    python3 scripts/auto_fix.py
                    git config user.email "jenkins@secureops.com"
                    git config user.name "Jenkins Bot"
                    git checkout -b auto-fix-vulnerabilities || git checkout auto-fix-vulnerabilities
                    git add app/requirements.txt
                    git commit -m "auto-fix: update vulnerable packages" || echo "Nothing to commit"
                    git push https://${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git auto-fix-vulnerabilities
                '''
            }
        }
        stage('Load Image into kind') {
            steps {
                sh 'kind load docker-image secureops-app:latest --name secureops-cluster'
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yaml --validate=false'
            }
        }
    }
    post {
        failure {
            echo 'Pipeline failed — CRITICAL vulnerabilities blocked deployment!'
        }
        success {
            echo 'Pipeline completed successfully — no critical vulnerabilities!'
        }
    }
}
