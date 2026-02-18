from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "replace_this_with_secure_key")

# DB CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2006@localhost/voting_db3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------- MODELS ----------

class Voter(db.Model):
    __tablename__ = "voters"
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    has_voted = db.Column(db.Boolean, default=False)
    aadhaar_filename = db.Column(db.String(255))  # <-- NEW
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)
    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)

class Candidate(db.Model):
    __tablename__ = "candidates"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    party = db.Column(db.String(120))

class Vote(db.Model):
    __tablename__ = "votes"
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey("voters.id"), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint("voter_id", name="uq_vote_voter"),)

# ---------- ADMIN CREDENTIALS ----------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ---------- FUNCTIONS ----------
def calculate_age(dob: date):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# ---------- ROUTES ----------

@app.route("/")
def home():
    return render_template("main.html")

# ----- REGISTER -----
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        voter_id = request.form["voter_id"]
        dob = datetime.strptime(request.form["dob"], "%Y-%m-%d").date()
        password = request.form["password"]

        if calculate_age(dob) < 18:
            return render_template("index.html", message="You must be 18+")

        exists = Voter.query.filter_by(voter_id=voter_id).first()
        if exists:
            return render_template("index.html", message="Voter already exists")

        v = Voter(name=name, voter_id=voter_id, dob=dob)
        v.set_password(password)

        # ---- Aadhaar Upload ----
        aadhaar_file = request.files.get('aadhaar')
        if aadhaar_file and aadhaar_file.filename != '':
            filename = secure_filename(aadhaar_file.filename)
            os.makedirs('static/aadhaar', exist_ok=True)
            save_path = os.path.join('static/aadhaar', filename)
            aadhaar_file.save(save_path)
            v.aadhaar_filename = filename

        db.session.add(v)
        db.session.commit()
        flash("Registration successful.")
        return redirect(url_for("login"))

    return render_template("index.html")

# ----- LOGIN -----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        voter_id = request.form["voter_id"]
        password = request.form["password"]

        v = Voter.query.filter_by(voter_id=voter_id).first()
        if not v or not v.check_password(password):
            return render_template("login.html", message="Invalid login")

        session["voter_id"] = v.id
        return redirect(url_for("vote"))

    return render_template("login.html")

# ----- VOTE -----
@app.route("/vote", methods=["GET", "POST"])
def vote():
    if "voter_id" not in session:
        return redirect(url_for("login"))

    voter = Voter.query.get(session["voter_id"])
    candidates = Candidate.query.all()

    if voter.has_voted:
        return render_template("vote.html", voted=True)

    if request.method == "POST":
        cid = int(request.form["candidate"])
        vote = Vote(voter_id=voter.id, candidate_id=cid)
        voter.has_voted = True
        db.session.add(vote)
        db.session.commit()

        return render_template("thankyou.html", voter=voter, candidate=Candidate.query.get(cid))

    return render_template("vote.html", voter=voter, candidates=candidates)

# ----- LOGOUT -----
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ---------- ADMIN ROUTES ----------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_dashboard"))

        return render_template("admin_login.html", message="Invalid admin login")

    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    voters = Voter.query.all()
    candidates = Candidate.query.all()
    return render_template("admin_dashboard.html", voters=voters, candidates=candidates)

@app.route("/admin/add_candidate", methods=["POST"])
def admin_add_candidate():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    name = request.form["name"]
    party = request.form["party"]
    c = Candidate(name=name, party=party)
    db.session.add(c)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/results")
def admin_results():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    results = db.session.query(Candidate, db.func.count(Vote.id).label("total"))\
        .outerjoin(Vote).group_by(Candidate.id).all()
    return render_template("results_admin.html", results=results)

@app.route("/admin/export")
def admin_export():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))

    results = db.session.query(Candidate.name, db.func.count(Vote.id))\
        .outerjoin(Vote).group_by(Candidate.id).all()

    csv_text = "candidate,total\n"
    for name, total in results:
        csv_text += f"{name},{total}\n"

    return app.response_class(
        csv_text,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=results.csv"}
    )

# ----- DB -----
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
