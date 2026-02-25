import os
from app.LoadAudio import transcrypt_files
from flask import Blueprint, render_template, request, jsonify, Flask, flash, redirect
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'app/audio_files'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'aac'}
ALLOWED_MIME = {"audio/mpeg", "audio/wav", "audio/aac"}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


main = Blueprint("main", __name__)
@main.route("/")
def home():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=files)


@main.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("q")
    response = f"recibi al consulta ahorita no puedo procesarla porque solo es texto plano para pruebas pero tu pregunta fue : {question}"

    return jsonify({
        "question": question,
        "answer": response
    })


@main.route("/charge_audio", methods=["POST"])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect("/")
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect("/")
    if not allowed_file(file.filename):
        flash("Wrong format the allowed formats are 'mp3', 'wav', 'aac'")
        return redirect("/")
    if file.mimetype not in ALLOWED_MIME:
        flash("This is not an audio file")
        return redirect("/")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        flash("Successfull upload "+ file.filename)
        return redirect("/")


@main.route("/delete_audio/<file_name>", methods=["GET"])
def delete_file(file_name):
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash("Successfull delete "+ file_name)
        return redirect("/")
    else:
        flash("Error on delete "+ file_name)
        return redirect("/")


