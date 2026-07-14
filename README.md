# 🗳️ Online Voting System

A secure and user-friendly **web-based Online Voting System** developed using **Python Flask and PostgreSQL** that enables voters to register, authenticate, and cast their votes digitally. The system provides an admin dashboard to manage candidates, monitor registered voters, view election results, and export voting data.

---

## 📌 Project Overview

The **Online Voting System** is designed to simplify the traditional voting process by providing a digital platform where eligible voters can register and participate in elections securely.

The system verifies voter details, prevents multiple voting attempts, maintains election records, and helps administrators efficiently manage the complete voting process through an interactive dashboard.

---

## 🚀 Features

### 👤 Voter Module

- Voter registration with personal details
- Secure password encryption
- Age verification (18+ eligibility check)
- Unique Voter ID validation
- Voter login authentication
- View available candidates
- Cast vote securely
- Prevent multiple voting by the same user
- Logout functionality

---

### 🛡️ Admin Module

- Secure admin login
- Admin dashboard
- View registered voters
- Monitor voting status
- Add new candidates
- Manage candidate details
- View election results
- Export voting results as CSV file

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- Jinja2 Template Engine

### Backend
- Python
- Flask Framework

### Database
- PostgreSQL
- SQLAlchemy ORM

### Security
- Password Hashing using Werkzeug
- Session-based authentication

---

## 📂 Project Structure

```
voting_app/
│
├── app.py
│
├── templates/
│   │
│   ├── index.html
│   ├── login.html
│   ├── vote.html
│   ├── thankyou.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── results_admin.html
│
├── static/
│   └── css/
│
├── requirements.txt
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/OnlineVotingSystem.git
```

Navigate into project folder:

```bash
cd OnlineVotingSystem
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

---

### 3. Install Required Libraries

```bash
pip install flask flask-sqlalchemy psycopg2-binary werkzeug
```

---

### 4. Configure Database

Create PostgreSQL database:

```
voting_db3
```

Update database configuration inside:

```
app.py
```

Example:

```python
postgresql://username:password@localhost/voting_db3
```

---

### 5. Run Application

Start Flask server:

```bash
python app.py
```

Application will run at:

```
http://127.0.0.1:5000/
```

---

## 🔑 Default Admin Login

```
Username:
admin

Password:
admin123
```

---

## 📊 System Workflow

```
Voter Registration
        |
        ↓
Voter Login Authentication
        |
        ↓
Candidate Selection
        |
        ↓
Vote Submission
        |
        ↓
Database Storage
        |
        ↓
Admin Dashboard Monitoring
        |
        ↓
Election Result Generation
```

---

## 🗄️ Database Tables

### Voters Table

Stores voter information:

- ID
- Voter ID
- Name
- Date of Birth
- Password Hash
- Voting Status
- Registration Date


### Candidates Table

Stores candidate information:

- Candidate ID
- Candidate Name
- Party Details


### Votes Table

Stores voting records:

- Vote ID
- Voter ID
- Candidate ID
- Timestamp

---

## 🔒 Security Features

- Password hashing
- Unique voter ID constraint
- One vote per voter restriction
- Session-based authentication
- Database validation
- Protected admin routes

---

## 📸 Application Screenshots

(Add your project screenshots here)

Example:

```
screenshots/
│
├── voter_registration.png
├── voter_login.png
├── voting_page.png
├── admin_dashboard.png
└── results.png
```

---

## 🔮 Future Enhancements

- Aadhaar-based voter verification
- OTP authentication
- Face recognition verification
- Blockchain-based vote storage
- Real-time election analytics
- Mobile application support
- Cloud deployment

---

## 👨‍💻 Developed By

**Sanjay D S**

Electronics and Communication Engineering

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.
