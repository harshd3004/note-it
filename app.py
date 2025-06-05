from flask import Flask,render_template,request,flash
from datetime import datetime,timezone
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'temp_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///noteit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000), nullable=False)
    time_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    time_modified = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

with app.app_context():
    db.create_all()

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/note-editor',methods=['GET','POST'])
def noteEditor():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']

        new_note = Note(title=title,content=content)
        db.session.add(new_note)
        db.session.commit()
        flash("Changes to note saved successfully", "success")
        return render_template('main_page.html')
    return render_template('note-editor.html')

if __name__ == "__main__":
    app.run(debug=True)