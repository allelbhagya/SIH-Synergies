from flask import Flask, render_template, send_file, request
from flask_sqlalchemy import SQLAlchemy
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import io

app = Flask(__name__)
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files_upload.db'   
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

admin = Admin(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    data = db.Column(db.LargeBinary)

with app.app_context():
    db.create_all()

def upload_files_to_db(static_folder_path):
    # List all files in the static folder
    files = os.listdir(static_folder_path)

    # Loop through the files and upload them to the database
    for filename in files:
        with open(os.path.join(static_folder_path, filename), 'rb') as file:
            file_data = file.read()
            new_file = File(name=filename, data=file_data)
            db.session.add(new_file)
    db.session.commit()

@app.route('/upload')
def upload():
    static_folder_path = 'C:\\Users\\DELL\\Desktop\\sih\\uploads'  
    upload_files_to_db(static_folder_path)
    return 'Files uploaded to the database.'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/school")
def school():
    #pdf_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("school.html")

@app.route("/university")
def university():
    return render_template("university.html")

@app.route("/industry")
def industry():
    return render_template("industry.html")

@app.route("/police")
def police():
    return render_template("police.html")

@app.route("/judi")
def judi():
    return render_template("judi.html")

@app.route("/not_available")
def not_Available():
    return render_template("not_av.html")

@app.route('/download/<int:id>')
def download_file(id):
    file = File.query.get(id)
    if file:
        return send_file(io.BytesIO(file.data),
                         download_name=file.name,
                         as_attachment=True)
    else:
        return "File not found", 404

@app.route("/not_translated")
def not_Translated():
    return render_template("not_tr.html")

if __name__ == '__main__': 
   app.run(debug=True)