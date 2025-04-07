import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize DB
def init_db():
    conn = sqlite3.connect('hospital.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        gender TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialty TEXT
    )''')
    cur.execute('''CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        date TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# Helper to get DB connection
def get_db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/stats')
def get_stats():
    conn = get_db_connection()
    cur = conn.cursor()

    patient_count = cur.execute('SELECT COUNT(*) FROM patients').fetchone()[0]
    doctor_count = cur.execute('SELECT COUNT(*) FROM doctors').fetchone()[0]
    appointment_count = cur.execute('SELECT COUNT(*) FROM appointments').fetchone()[0]

    conn.close()

    return jsonify({
        'patients': patient_count,
        'doctors': doctor_count,
        'appointments': appointment_count
    })


@app.route('/api/patients', methods=['GET', 'POST'])
def handle_patients():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        data = request.get_json()
        cur.execute('INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)',
                    (data['name'], data['age'], data['gender']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Patient added!'}), 201

    patients = cur.execute('SELECT * FROM patients').fetchall()
    conn.close()
    return jsonify([dict(row) for row in patients])

@app.route('/api/patient/<int:id>', methods=['GET'])
def get_patient(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM patients WHERE id = ?', (id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'Patient not found'}), 404

@app.route('/api/patients/<int:id>', methods=['GET', 'PUT'])
def get_or_update_patient(id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'GET':
        patient = cur.execute('SELECT * FROM patients WHERE id = ?', (id,)).fetchone()
        conn.close()
        if patient:
            return jsonify(dict(patient))
        return jsonify({'error': 'Patient not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        cur.execute('UPDATE patients SET name = ?, age = ?, gender = ? WHERE id = ?',
                    (data['name'], data['age'], data['gender'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Patient updated'})
    
# Example with SQLAlchemy:
@app.route('/api/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM patients WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Patient deleted'}), 200



@app.route('/api/doctors', methods=['GET', 'POST'])
def handle_doctors():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        data = request.get_json()
        cur.execute('INSERT INTO doctors (name, specialty) VALUES (?, ?)',
                    (data['name'], data['specialty']))
        doctor_id = cur.lastrowid  # get the ID of the new doctor
        conn.commit()
        conn.close()
        return jsonify({
    'id': doctor_id,
    'name': data['name'],
    'specialty': data['specialty']
}), 201

    doctors = cur.execute('SELECT * FROM doctors').fetchall()
    conn.close()
    return jsonify([dict(row) for row in doctors])

@app.route('/api/doctors/<int:id>', methods=['GET'])
def get_doctor(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM doctors WHERE id = ?', (id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'Doctor not found'}), 404


@app.route('/api/doctors/<int:id>', methods=['GET', 'PUT'])
def handle_doctor(id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'GET':
        doctor = cur.execute('SELECT * FROM doctors WHERE id = ?', (id,)).fetchone()
        conn.close()
        if doctor:
            return jsonify(dict(doctor))
        return jsonify({'error': 'Doctor not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()
        cur.execute('UPDATE doctors SET name = ?, specialty = ? WHERE id = ?',
                    (data['name'], data['specialty'], id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Doctor updated successfully'})

@app.route('/api/doctors/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM doctors WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Doctor deleted!'}), 200



@app.route('/api/appointments', methods=['GET', 'POST'])
def handle_appointments():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        data = request.get_json()
        cur.execute('INSERT INTO appointments (patient_id, doctor_id, date) VALUES (?, ?, ?)',
                    (data['patient_id'], data['doctor_id'], data['date']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Appointment booked!'}), 201

    appointments = cur.execute('SELECT * FROM appointments').fetchall()
    conn.close()
    return jsonify([dict(row) for row in appointments])

@app.route('/api/apppointmentts/<int:id>', methods=['GET'])
def get_appointmentt(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM appointments WHERE id = ?', (id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({'error': 'Appointment not found'}), 404

@app.route('/api/appointments/<int:id>', methods=['GET'])
def get_appointment(id):
    conn = get_db_connection()
    cur = conn.cursor()
    appointment = cur.execute('SELECT * FROM appointments WHERE id = ?', (id,)).fetchone()
    conn.close()
    if appointment is None:
        return jsonify({'error': 'Appointment not found'}), 404
    return jsonify(dict(appointment))


@app.route('/api/appointments/<int:id>', methods=['PUT'])
def update_appointment(id):
    conn = get_db_connection()
    cur = conn.cursor()
    data = request.get_json()
    
    cur.execute('UPDATE appointments SET patient_id = ?, doctor_id = ?, date = ? WHERE id = ?',
                (data['patient_id'], data['doctor_id'], data['date'], id))
    
    conn.commit()
    conn.close()
    return jsonify({'message': 'Appointment updated successfully'})

@app.route('/api/appointments/<int:id>', methods=['DELETE'])
def delete_appointments(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM appointments WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Appointments deleted!'}), 200

@app.route('/api/fullappointments')
def get_full_appointments():
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute('''
        SELECT 
            a.id as id,
            a.date as date,
            p.name as patient,
            d.doctor as doctor
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
    ''')

    rows = cur.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows])


@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Flask!"})

if __name__ == '__main__':
    app.run(debug=True)
