# Back-end for the fake-detector app
# By: Wanga Mulaudzi
# July 2024

# Import statements
from api.upload import handle_image_upload # Import API call that handles an image upload
from flask import Flask, request, jsonify # For making API calls
from flask_cors import CORS # For routing
from google.oauth2 import service_account # To access service account details
from google.cloud import storage, secretmanager # For accessing the keras cnn model and google cloud secrets
import os # Operating system tasks
import tempfile # For temporary caching
import tensorflow as tf # For the CNN model
import toml # For extracting json from toml
import json

# Initialize the flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:8501", "http://127.0.0.1:8501", "http://192.168.178.52:8501"]}}, supports_credentials=True)

def access_secret_version(secret_id):
    """
    Access the payload of a secret version.
    """
    client = secretmanager.SecretManagerServiceClient()
    project_id = "fake-detector-427308"
    secret_version_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    response = client.access_secret_version(name=secret_version_name)
    secret_payload = response.payload.data.decode('UTF-8')

    return secret_payload

def get_service_account_credentials(json_string):
    """
    Parses JSON string from TOML and returns service account credentials.
    """
    # Parse the TOML formatted JSON string
    toml_data = toml.loads(json_string)
    json_string = toml_data["google"]["credentials"]

    # Load the JSON data into a dictionary
    credentials_info = json.loads(json_string)

    # Create credentials from the JSON dictionary
    credentials = service_account.Credentials.from_service_account_info(credentials_info)

    return credentials

def get_storage_client():
    """
    Returns the storage client for the specified project with credentials
    """
    secret_payload = access_secret_version("streamlit_secrets")
    credentials = get_service_account_credentials(secret_payload)
    client = storage.Client(credentials=credentials)

    return client

def load_keras_model():
    """
    Loads the stored keras model from google cloud storage.

    Returns:
        The loaded model
    """
    storage_client = get_storage_client()
    bucket = storage_client.get_bucket("fake-detector")

    blob = bucket.blob("models/final_model.keras")

    # Create a temporary file
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_model_path = os.path.join(temp_dir, "final_model.keras")

        blob.download_to_filename(temp_model_path)

        # Load the model
        model = tf.keras.models.load_model(temp_model_path)

    return model

# Load the model when the Flask app starts
model = load_keras_model()

#####################
# Deepfake Detector #
#####################

# API call for an uploaded image
@app.route("/api/upload_and_predict", methods=["POST"])
def upload_image():
    file = request.files["file"]

    image_bytes = file.read()

    prediction = handle_image_upload(model, image_bytes)

    return prediction

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
