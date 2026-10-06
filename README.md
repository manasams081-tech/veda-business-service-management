# Veda Nexus — Business & Service Management System

A major-project-level Python web application for managing technology services, programs, customers, inquiries and business reports using only the technologies specified in the Veda Technology task: **Python, VS Code/PyCharm, JSON/CSV, Git and GitHub**.

## What this project delivers

- Executive dashboard with live operational metrics
- Service management with categories, owners, priority and status
- Program management for training, internships and technology programs
- Customer/service relationship management
- Customer inquiry and service-request tracking
- Search and filtering across modules
- Inquiry status workflow
- JSON-based persistent data storage
- CSV exports for all major datasets
- Business reporting page
- Clean reusable Jinja templates
- Responsive, original Veda-inspired interface
- Input validation and exception handling
- Small JSON API summary endpoint

## Project structure

```text
veda_business_service_management/
├── app.py
├── requirements.txt
├── run.bat
├── README.md
├── .gitignore
├── data/
│   ├── services.json
│   ├── programs.json
│   ├── customers.json
│   └── inquiries.json
├── app/
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── services.html
│   │   ├── programs.html
│   │   ├── customers.html
│   │   ├── inquiries.html
│   │   ├── reports.html
│   │   └── error.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
└── docs/
    └── PROJECT_NOTES.md
```

## Windows terminal setup

Open **Command Prompt or PowerShell** inside the extracted project folder.

### 1. Create virtual environment

```powershell
py -3.12 -m venv .venv
```

If `py -3.12` is not available but `python` points to Python 3.12, use:

```powershell
python -m venv .venv
```

### 2. Activate it

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Command Prompt:

```cmd
.venv\Scripts\activate
```

### 3. Install dependency

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run

```powershell
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

### 5. Stop the application

Press `CTRL + C` in the terminal.

## GitHub push sequence

Recommended repository name:

`veda-task-29-business-service-management-system`

Suggested description:

`Major Python web application for technology service, program, customer, inquiry and business report management using Flask, JSON and CSV.`

After creating an **empty public repository** on GitHub, run these commands from the project folder:

```powershell
git init
git add .
git commit -m "Initial commit - Veda Business Service Management System"
git branch -M main
git remote add origin https://github.com/manasams081-tech/veda-task-29-business-service-management-system.git
git push -u origin main
```

If Git asks for authentication, complete GitHub's normal browser/sign-in flow. Do not paste a password into the terminal.

## If `remote origin already exists`

Run:

```powershell
git remote -v
git remote set-url origin https://github.com/manasams081-tech/veda-task-29-business-service-management-system.git
git push -u origin main
```

## Verify the push

```powershell
git status
git remote -v
git log --oneline -1
```

The repository should show the application files, `data` folder, `app/templates`, `app/static`, README and requirements file.

## Important task alignment

The application uses Python, JSON/CSV persistence, Git and GitHub. It does not connect to private Veda Technology production data and all sample records are synthetic.
