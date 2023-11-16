import json
from google.cloud import storage
from google.cloud import firestore

storage_client = storage.Client()
firestore_client = firestore.Client()

def hello_gcs(event, context):
    
    # Descarga el archivo desde Cloud Storage
    blob = storage_client.bucket(event["bucket"]).get_blob(event["name"])
    content = blob.download_as_text()
    file_name = event['name']
    document_name = file_name.split('.')[0]
    # Lee y muestra el contenido del archivo JSON
    data = json.loads(content)
    print(event)
    print(data)
    firestore_client.collection("diegocol").document(document_name).set(data)