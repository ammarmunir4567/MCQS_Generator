from dotenv import load_dotenv
from dotenv import dotenv_values
from flask import Flask
from flask_cors import CORS
from MCQS import generate

load_dotenv()

config = dotenv_values(".env")
app = Flask(__name__)

# Enable CORS for all origins and routes
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/generate', methods=['POST'])
def gen():
    return generate()

if __name__ == '__main__':
    app.run(port=8000, debug=True)
