import os
import subprocess
import hashlib

# Hardcoded secrets - Gitleaks will catch this
API_KEY = "sk-1234567890abcdef"
DB_PASSWORD = "supersecretpassword123"
AWS_SECRET = "AKIAIOSFODNN7EXAMPLE"

# SQL Injection vulnerability - Semgrep will catch this
def get_user(user_input):
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    return query

# Command injection - Semgrep will catch this
def run_command(user_input):
    os.system("ls " + user_input)
    subprocess.call("echo " + user_input, shell=True)

# Weak hashing - Semgrep will catch this
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()

# Debug mode on - Semgrep will catch this
def start_app():
    app.run(debug=True, host="0.0.0.0")
# test
