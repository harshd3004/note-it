from flask import Flask,render_template,request,flash,redirect,url_for
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
    time_created = db.Column(db.DateTime, default=datetime.now)
    time_modified = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

with app.app_context():
    db.create_all()

@app.route('/')
def main_page():
    notes = Note.query.all()
    return render_template('main_page.html',notes=notes)

@app.route('/register')
def register():
    return render_template('register.html')

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

        if note:
            note.title = title
            note.content = content
        else : 
            new_note = Note(title=title,content=content)
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