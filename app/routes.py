from flask import Blueprint, render_template, request, jsonify

main = Blueprint("main", __name__)
@main.route("/")
def home():
    return render_template("index.html")


@main.route("/ask", methods=["GET"])
def ask():
    question = request.args.get("q")
    response = f"recibi al consulta ahorita no puedo procesarla porque solo es texto plano para pruebas pero tu pregunta fue : {question}"

    return jsonify({
        "question": question,
        "answer": response
    })

