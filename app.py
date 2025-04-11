from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/courses')
def get_courses():
    with open('courses.json') as f:
        courses = json.load(f)
    return jsonify(courses)

@app.route('/api/testimonials')
def get_testimonials():
    with open('testimonials.json') as f:
        testimonials = json.load(f)
    return jsonify(testimonials)

if __name__ == '__main__':
    app.run(debug=True)
