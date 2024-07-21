# Fake Detector Backend

This is the backend service for the Fake Detector application, which uses AI to determine if an image is real or artificially generated.

The frontend repo can be found [here](https://github.com/wangamulaudzi/fake-detector-frontend/).

## Local Setup

1. Clone the repository:
`git clone <repository-url>`
`cd fake-news-backend`

2. Set up a virtual environment:
`pyenv virtualenv 3.10.6 <environment-name>`
`pyenv local <environment-name>`

3. Install dependencies:
`pip install -r requirements.txt`

4. Run the application:
`python fake-detector.py`

The server should now be running on `http://localhost:8080`.

## API Endpoints

- `POST /api/upload_and_predict`: Endpoint to upload an image and get prediction.

For more details on the API, refer to the `fake-detector.py` file.

## Troubleshooting

For local debugging, set `debug=True` in the `app.run()` call in `fake-detector.py`.
