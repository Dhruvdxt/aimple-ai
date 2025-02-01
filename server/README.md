# Commands to clone this repository
git clone https://github.com/Dhruvdxt/aimple-ai
cd aimple-ai

# Commands to install all requirements
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Commands to push code to the repository

>> Connect with the remote server once
git remote add origin https://github.com/Dhruvdxt/aimple-ai

>> To switch branch
git branch -M main

>> Run
git add .
git commit -m "commit-messege"
git push -u origin main

# Command to freeze all requirements
Note: Run this command in root dir aimple-ai
pip freeze > requirements.txt