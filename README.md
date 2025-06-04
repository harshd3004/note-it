# 📝 Note-It
A minimal, multi-user **note-taking web app** built with **Flask** , inspired by Google Keep. Users can register, log in, and manage their personal notes securely.

---

## 🚀 Features

- 🧑‍💻 User Registration & Login
- 🔐 Secure password hashing with Werkzeug
- 🗒️ Create, View, Edit, and Delete personal notes
- 👤 User-specific access — each user sees only their notes
- 🎨 Clean and responsive UI with HTML/CSS (Bootstrap)
- 🛠️ SQLite for development 

---

## 📂 Tech Stack

- **Backend**: Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, Jinja Templates
- **ORM**: SQLAlchemy


---

## 🏁 Getting Started

### 1. Clone the repo
git clone https://github.com/harshd3004/note-it.git
cd note-it
### 2. Set up environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
### 3. Run the app
python app.py


## 🗃️ Database
Models: User, Note

Each Note is linked to a User via a one-to-many relationship.