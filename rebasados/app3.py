from flask import Flask, render_template, request, redirect
from google.cloud import storage, firestore
import json
import random
import datetime
import time

app = Flask(__name__)

storage_client = storage.Client()
bucket_name = 'mi-bucket-proyecto'
bucket = storage_client.bucket(bucket_name)

firestore_client = firestore.Client()

today = datetime.date.today().strftime('%Y-%m-%d')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")

        # Verifica que los campos no estén vacíos antes de procesar
        if nombre and email:
            usuario = {
                'ID': random.randint(100000, 999999),
                'Nombre': nombre,
                'Correo electrónico': email,
                'Fecha de registro': today
            }

            timestamp = int(time.time())
            file_name = f'usuarios_{timestamp}.json'

            blob = bucket.blob(file_name)
            blob.upload_from_string(data=json.dumps(usuario), content_type='application/json')

            #registro_name = f"registro-{timestamp}"
            #firestore_client.collection("bbdd-gcp").document(registro_name).set(usuario)

        time.sleep(5)
        return redirect("/data")

    return render_template("index.html")


@app.route("/data")
def data():
    docs = firestore_client.collection("bbdd-gcp").stream()
    items = [doc.to_dict() for doc in docs]
    return render_template("data.html", items=items)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)