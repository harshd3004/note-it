from flask import Flask,render_template,request,flash,redirect,url_for
from datetime import datetime,timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, UserMixin, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'temp_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///noteit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100),unique=True, nullable=False)
    passwd = db.Column(db.String(100), nullable=False)
    notes = db.relationship('Note', backref='user', lazy=True)
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000), nullable=False)
    time_created = db.Column(db.DateTime, default=datetime.now)
    time_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

with app.app_context():
    db.create_all()

@app.route('/')
def main_page():
    if current_user.is_authenticated:
        notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.time_modified.desc()).all()
    else:
        notes = None
    return render_template('main_page.html',notes=notes)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        passwd = generate_password_hash(request.form.get('passwd'))

        errors=[]
        if not email or '@' not in email:
            errors.append("Valid email is required.")
        if len(passwd) < 8:
            errors.append("Password must be at least 8 characters.")
        
        if errors:
            flash('<br>'.join(errors),'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists.', 'danger')
            return redirect(url_for('register'))

        user = User(name=name, email=email, passwd=passwd)
        db.session.add(user)
        db.session.commit()
        flash("User Registration Sucessfull, You can now Login!",'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        passwd = request.form.get('passwd')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.passwd, passwd):
            login_user(user)
            flash("Login Sucessfull !!",'success')
            return redirect(url_for('main_page'))
        else:
            flash("Invalid Credentials",'danger')
    return render_template('login.html')

@login_required
@app.route('/logout')
def logout():
    logout_user()
    flash("User Logged out",'success')
    return redirect(url_for('login'))

@login_required
@app.route('/note-editor',methods=['GET','POST'])
@app.route('/note-editor/<int:note_id>',methods=['GET','POST'])
def noteEditor(note_id = None):
    note = None
    if note_id:
        note = Note.query.get(note_id)
    if request.method == "POST":
        note_id = request.form.get('note_id')
        if note_id:
            note = Note.query.get(int(note_id))
        title = request.form['title']
        content = request.form['content']
        user_id = current_user.id
        if note:
            note.title = title
            note.content = content
        else : 
            new_note = Note(title=title,content=content,user_id=user_id)
            db.session.add(new_note)
        db.session.commit()
        flash("Changes to note saved successfully", "success")
        return redirect(url_for('main_page'))
    return render_template('note-editor.html',note=note)

@app.route('/delete-note/<int:id>')
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    flash("Note deleted successfully!", "success")
    return redirect(url_for('main_page'))

if __name__ == "__main__":
    app.run(debug=True)