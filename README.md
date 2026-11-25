<<<<<<< HEAD
# CampusFind — Campus Lost & Found Portal

A responsive full-stack college project for reporting lost belongings and found items.

## Features
- Report Lost or Found items
- Browse and search open reports
- Filter by type and category
- Item detail pages
- Submit claim requests
- Admin demo dashboard to view reports and claims and mark reports resolved
- SQLite database created automatically

## Stack
HTML5, CSS3, JavaScript, Python Flask, SQLite

## Run on Windows
1. Install Python 3.10+.
2. Extract the ZIP and open the folder in VS Code.
3. Open Terminal in the folder:
   ```powershell
   python -m venv venv
   ```
4. Activate (PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt: `venv\\Scripts\\activate.bat`. Or continue without activation and run `python -m pip`.
5. Install:
   ```powershell
   python -m pip install -r requirements.txt
   ```
6. Start:
   ```powershell
   python app.py
   ```
7. Visit http://127.0.0.1:5000

## Demo/admin
Open `/admin` to see all reports and submitted claims. This prototype does not include authentication, so do not deploy the admin page publicly without adding login and access control.

## Privacy / project note
Use demo contact details during presentations. The app stores user-submitted contact information locally in `campusfind.db`. A production version should add authentication, privacy controls, moderation, and secure deployment.
=======
# CampusFind-Lost-and-Found
A college Lost &amp; Found web portal built using HTML, CSS, JavaScript, Python Flask, and SQLite.
>>>>>>> 9a4996094967ab58f6a7df1d227822cf73276f47
