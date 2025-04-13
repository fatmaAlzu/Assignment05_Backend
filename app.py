from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

# Global list to store student records
students = []

# (Old) Courses endpoint with /api prefix (for legacy use)
@app.route('/api/courses')
def get_api_courses():
    with open('courses.json') as f:
        courses = json.load(f)
    return jsonify(courses)

# Get All Courses API: GET /courses
@app.route('/courses', methods=['GET'])
def get_all_courses():
    with open('courses.json') as f:
        courses = json.load(f)
    return jsonify(courses)


def load_testimonials():
    """Helper function to load testimonials and select two random testimonials."""
    with open('testimonials.json') as f:
        testimonials = json.load(f)
    if len(testimonials) >= 2:
        return random.sample(testimonials, 2)
    return testimonials


@app.route('/testimonials', methods=['GET'])
@app.route('/api/testimonials', methods=['GET'])
def testimonials_api():
    return jsonify(load_testimonials())


# Student Registration API: POST /register
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Check if the username already exists
    for student in students:
        if student['username'] == username:
            return jsonify({'success': False, 'message': 'Username already taken.'}), 400

    new_student = {
        'id': len(students) + 1,
        'username': username,
        'password': password,  # Note: In production, hash your passwords.
        'email': email,
        'enrolled_courses': []
    }
    students.append(new_student)
    return jsonify({'success': True, 'message': 'Registration successful.'}), 200

# Login API: POST /login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    for student in students:
        if student['username'] == username and student['password'] == password:
            return jsonify({
                'success': True,
                'message': 'Login successful.',
                'student_id': student['id']
            }), 200

    return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

# Enroll Courses API: POST /enroll/<student_id>
@app.route('/enroll/<int:student_id>', methods=['POST'])
def enroll_course(student_id):
    course_data = request.get_json()
    if not course_data:
        return jsonify({'success': False, 'message': 'No course information provided.'}), 400

    for student in students:
        if student['id'] == student_id:
            student['enrolled_courses'].append(course_data)
            return jsonify({'success': True, 'message': 'Course enrollment successful.'}), 200

    return jsonify({'success': False, 'message': 'Student not found.'}), 404

# Delete Courses API: DELETE /drop/<student_id>
@app.route('/drop/<int:student_id>', methods=['DELETE'])
def drop_course(student_id):
    course_data = request.get_json()
    if not course_data:
        return jsonify({'success': False, 'message': 'No course information provided.'}), 400

    for student in students:
        if student['id'] == student_id:
            if course_data in student['enrolled_courses']:
                student['enrolled_courses'].remove(course_data)
                return jsonify({'success': True, 'message': 'Course dropped successfully.'}), 200
            else:
                return jsonify({'success': False, 'message': 'Course not found in student enrollment.'}), 404

    return jsonify({'success': False, 'message': 'Student not found.'}), 404

# Get Student Courses API: GET /student_courses/<student_id>
@app.route('/student_courses/<int:student_id>', methods=['GET'])
def get_student_courses(student_id):
    # Search for the student by ID in the global students list.
    for student in students:
        if student['id'] == student_id:
            # Return the list of courses the student is enrolled in.
            return jsonify(student['enrolled_courses'])
    # If the student is not found, return an empty list.
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5001)
