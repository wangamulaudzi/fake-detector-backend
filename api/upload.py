# Upload API call for the deepfake detector
# By: Wanga Mulaudzi
# July 2024

# Import statements
from flask import jsonify # For creating the APIs
import io # For reading bytes
import numpy as np # For numerical operations
from PIL import Image # For reading bytes into images

def preprocess_image(image_bytes, target_size=(256, 256)):
    """
    Preprocess the uploaded image so it can be parsed to the model.

    Parameters:
        image_bytes: The raw image bytes that were uploaded from the frontend
        target_size: The expected size of the image based on the CNN model's input layer

    Returns:
        The preprocessed image
    """
    # Open the image with PIL
    image = Image.open(io.BytesIO(image_bytes))

    # Convert the image to RGB to ensure consistent color channels
    image = image.convert("RGB")

    # Resize the image
    image = image.resize(target_size)

    # Convert the image to a NumPy array
    image_array = np.array(image)

    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)

    return image_array

# For when a user uploads an image
def handle_image_upload(deepfake_model, image_bytes):
    """
    Process the image bytes and return whether image is fake or real

    Parameters:
        deepfake_model: The keras model that is loaded in the backend
        image_bytes: The bytes of the uploaded image

    Returns:
        True or False
    """

    # Preprocess the image
    preprocessed_image = preprocess_image(image_bytes)

    try:
        # Predictions
        predictions = deepfake_model.predict(preprocessed_image)

        # Softmax output will have two probabilities
        fake_probability = predictions[0][0]
        real_probability = predictions[0][1]

        # Determine the class based on higher probability
        result = "Real" if real_probability > fake_probability else "Deepfake"

        return jsonify({
            "message": "Image successfully received.",
            "prediction": result,
            "real_probability": float(real_probability),
            "fake_probability": float(fake_probability)
            }), 200

    except:
        return jsonify({
            "message": "Invalid image",
            "prediction": "Invalid image",
            "real_probability": 0,
            "fake_probability": 0
            }), 500
