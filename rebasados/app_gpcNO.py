"""
Aplicación para página web conectada a una base de datos dynamoDB,
un bucket S3, una lambda que actualiza la base de datos con
los json subidos al bucket, y una instancia de EC2 para desplegar
la web.
La página web tendrá dos endpoints. La página de inicio, que
contiene el formulario para agregar información a la base de datos,
y la página de data, que contiene la tabla de usuarios de la base
de datos.
"""

from flask import Flask, render_template, request, redirect
from google.cloud import storage
from google.cloud import firestore

import json
import random
import datetime
import time

# Create a client for Google Cloud Storage
client = storage.Client(project="thebridgecloudsep23")
db = firestore.Client(project="thebridgecloudsep23")


# Get the GCS bucket

bucket = client.get_bucket("bucketej")


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Definición: Endpoint para la página de inicio de la web. Contiene un formulario.

    Form: Nombre - Nombre insertado por el usuario.
    Form: Correo electrónico - email insertado por el usuario.

    Return: index.html
    """
    if request.method == "POST":
        # Creamos un diccionario con los datos del usuario
        usuario = {
            'ID': random.randint(100000, 999999),
            'Nombre': request.form.get("nombre"),               # Dato procedente de la web
            'Correo electrónico': request.form.get("email"),    # Dato procedente de la web
            'Fecha de registro': today                          # Dato procedente de la variable creada arriba
        }

        # Guardamos los datos del usuario en un archivo JSON
        
        blob = bucket.blob(f'usuarios{today}.json')
        blob.upload_from_string(json.dumps(usuario))
        time.sleep(5)
        flash('¡Registro exitoso!', 'success')
    
        return redirect("/data")

    else:
        return render_template("index.html")


@app.route("/data")
def data():
    """
    Definición: Endpoint para la página de la tabla de usuarios.

    Items - diccionario de datos extraídos de la base de datos

    return: data.html
    """

      # Obtener todos los documentos de la colección 'usuarios'
    usuarios_ref = db.collection('usuarios')
    docs = usuarios_ref.stream()

    # Convertir los documentos a un formato serializable (diccionario)
    items = [doc.to_dict() for doc in docs]

    return render_template("data.html", items=items)


if __name__ == '__main__':
    # Ejecuta la aplicación
    app.run(host="0.0.0.0", port=8080, debug=True)