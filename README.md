# Commands to clone this repository
git clone https://github.com/aimpleai-org/user_management_and_auth_service.git
cd user_management_and_auth_service

# Commands to install all requirements
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Commands to push code to the repository

>> Connect with the remote server once
git remote add origin https://github.com/aimpleai-org/user_management_and_auth_service.git

>> To switch branch
git checkout -b <branch_name>

>> Run
git add .
git commit -m "commit-messege"
git push -u origin <branch_name>

# Command to freeze all requirements
NOTE: Run this command in root dir aimple-ai
Run: pip freeze > requirements.txt

# Command to run the server
NOTE: Before running the server, make sure that your localhost MySQL server is running and that a database is created with the name "aimple_ai_db".
You can create database using MySQL Workbench application.

>> Run
uvicorn server.main:app --reload
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload

# Command to run the redis server
docker run --name redis-server -d -p 6379:6379 redis