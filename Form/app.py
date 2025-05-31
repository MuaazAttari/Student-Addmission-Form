from flask import Flask, render_template, request, redirect, flash
import os
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Uploads folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Excel file
EXCEL_FILE = 'admissions.xlsx'

# Columns for Excel
columns = [
    'Timestamp', 'Full Name', "Father's Name", 'DOB', 'Gender', 'CNIC',
    'Nationality', 'Religion', 'Contact', 'Email', 'Address',
    'Qualification', 'Institute', 'Course',
    'Photo Path', 'CNIC File Path'
]

# If Excel file doesn't exist, create it
if not os.path.exists(EXCEL_FILE):
    pd.DataFrame(columns=columns).to_excel(EXCEL_FILE, index=False)


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = {
        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Full Name': request.form['name'],
        "Father's Name": request.form['father_name'],
        'DOB': request.form['dob'],
        'Gender': request.form['gender'],
        'CNIC': request.form['cnic'],
        'Nationality': request.form['nationality'],
        'Religion': request.form['religion'],
        'Contact': request.form['contact'],
        'Email': request.form['email'],
        'Address': request.form['address'],
        'Qualification': request.form['qualification'],
        'Institute': request.form['institute'],
        'Course': request.form['course'],
    }

    # Save photo
    photo = request.files['photo']
    cnic_file = request.files['cnic_file']

    photo_path = os.path.join(UPLOAD_FOLDER, f"{data['Full Name'].replace(' ', '_')}_photo_{datetime.now().timestamp()}.{photo.filename.split('.')[-1]}")
    cnic_path = os.path.join(UPLOAD_FOLDER, f"{data['Full Name'].replace(' ', '_')}_cnic_{datetime.now().timestamp()}.{cnic_file.filename.split('.')[-1]}")

    photo.save(photo_path)
    cnic_file.save(cnic_path)

    data['Photo Path'] = photo_path
    data['CNIC File Path'] = cnic_path

    # Load and append data to Excel
    df = pd.read_excel(EXCEL_FILE)
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

    flash('Form submitted successfully!', 'success')
    return render_template('success.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)

