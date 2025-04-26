from flask import Flask
from flask_cors import CORS
from routes.predict import predict_blueprint

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Register blueprint
app.register_blueprint(predict_blueprint, url_prefix='/predict')

@app.route('/')
def home():
    return {"message": "Stock Prediction Service is Running!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
