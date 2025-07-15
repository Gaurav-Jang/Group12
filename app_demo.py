from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import json
from datetime import datetime
import bcrypt

# Simple in-memory storage for demo (replace with MongoDB in production)
users_data = {
    'admin@healthcare.com': {
        '_id': '1',
        'email': 'admin@healthcare.com',
        'password': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()),
        'user_type': 'admin',
        'first_name': 'System',
        'last_name': 'Administrator',
        'phone': '+1234567890',
        'is_active': True
    },
    'doctor@healthcare.com': {
        '_id': '2',
        'email': 'doctor@healthcare.com',
        'password': bcrypt.hashpw('doctor123'.encode('utf-8'), bcrypt.gensalt()),
        'user_type': 'doctor',
        'first_name': 'Dr. John',
        'last_name': 'Smith',
        'phone': '+1234567891',
        'specialization': 'Neurology',
        'approved_by_admin': True,
        'is_active': True
    },
    'patient@healthcare.com': {
        '_id': '3',
        'email': 'patient@healthcare.com',
        'password': bcrypt.hashpw('patient123'.encode('utf-8'), bcrypt.gensalt()),
        'user_type': 'patient',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'phone': '+1234567892',
        'date_of_birth': '1990-01-01',
        'gender': 'Female',
        'is_active': True
    }
}

appointments_data = []
predictions_data = []

app = Flask(__name__)
app.secret_key = 'demo-secret-key-change-in-production'

def verify_password(password, hashed_password):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def get_current_user():
    """Get current user from session"""
    if 'user_email' in session:
        return users_data.get(session['user_email'])
    return None

@app.context_processor
def inject_user():
    """Make current user available in all templates"""
    return dict(current_user=get_current_user())

@app.route('/')
def index():
    """Home route - redirect based on user type"""
    if 'user_email' in session:
        user = get_current_user()
        if user:
            if user['user_type'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user['user_type'] == 'doctor':
                return redirect(url_for('doctor_dashboard'))
            elif user['user_type'] == 'patient':
                return redirect(url_for('patient_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        if not email or not password or not user_type:
            flash('Please fill in all fields.', 'error')
            return render_template('auth/login.html')
        
        # Find user
        user = users_data.get(email)
        if not user:
            flash('Invalid email or password.', 'error')
            return render_template('auth/login.html')
        
        # Check user type
        if user['user_type'] != user_type:
            flash('Invalid user type selected.', 'error')
            return render_template('auth/login.html')
        
        # Verify password
        if not verify_password(password, user['password']):
            flash('Invalid email or password.', 'error')
            return render_template('auth/login.html')
        
        # Login successful
        session['user_email'] = email
        session['user_type'] = user['user_type']
        session['user_name'] = f"{user['first_name']} {user['last_name']}"
        
        flash(f'Welcome back, {user["first_name"]}!', 'success')
        
        # Redirect based on user type
        if user_type == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif user_type == 'doctor':
            return redirect(url_for('doctor_dashboard'))
        elif user_type == 'patient':
            return redirect(url_for('patient_dashboard'))
    
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    """Logout and redirect to login page"""
    user_name = session.get('user_name', 'User')
    session.clear()
    flash(f'Goodbye, {user_name}!', 'info')
    return redirect(url_for('login'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    user = get_current_user()
    if not user or user['user_type'] != 'admin':
        flash('Admin access required.', 'error')
        return redirect(url_for('login'))
    
    stats = {
        'total_doctors': len([u for u in users_data.values() if u['user_type'] == 'doctor']),
        'approved_doctors': len([u for u in users_data.values() if u['user_type'] == 'doctor' and u.get('approved_by_admin', False)]),
        'pending_doctors': len([u for u in users_data.values() if u['user_type'] == 'doctor' and not u.get('approved_by_admin', False)]),
        'total_predictions': len(predictions_data),
        'reviewed_predictions': 0
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/doctor/dashboard')
def doctor_dashboard():
    """Doctor dashboard"""
    user = get_current_user()
    if not user or user['user_type'] != 'doctor':
        flash('Doctor access required.', 'error')
        return redirect(url_for('login'))
    
    stats = {
        'total_appointments': len(appointments_data),
        'pending_appointments': 0,
        'total_predictions': len(predictions_data),
        'pending_reviews': 0
    }
    
    return render_template('doctor/dashboard.html', stats=stats, recent_appointments=[])

@app.route('/patient/dashboard')
def patient_dashboard():
    """Patient dashboard"""
    user = get_current_user()
    if not user or user['user_type'] != 'patient':
        flash('Patient access required.', 'error')
        return redirect(url_for('login'))
    
    stats = {
        'total_appointments': 0,
        'upcoming_appointments': 0,
        'total_scans': 0,
        'recent_scans': 0
    }
    
    return render_template('patient/dashboard.html', stats=stats, recent_appointments=[])

@app.route('/patient/tumor_detection')
def tumor_detection():
    """Patient tumor detection page"""
    user = get_current_user()
    if not user or user['user_type'] != 'patient':
        flash('Patient access required.', 'error')
        return redirect(url_for('login'))
    
    return render_template('patient/tumor_detection.html')

@app.route('/patient/appointments')
def patient_appointments():
    """Patient appointments page"""
    user = get_current_user()
    if not user or user['user_type'] != 'patient':
        flash('Patient access required.', 'error')
        return redirect(url_for('login'))
    
    doctors = [u for u in users_data.values() if u['user_type'] == 'doctor' and u.get('approved_by_admin', False)]
    return render_template('patient/appointments.html', appointments=[], doctors=doctors)

@app.route('/patient/results')
def patient_results():
    """Patient results page"""
    user = get_current_user()
    if not user or user['user_type'] != 'patient':
        flash('Patient access required.', 'error')
        return redirect(url_for('login'))
    
    return render_template('patient/results.html', predictions=[])

@app.route('/patient/profile')
def patient_profile():
    """Patient profile page"""
    user = get_current_user()
    if not user or user['user_type'] != 'patient':
        flash('Patient access required.', 'error')
        return redirect(url_for('login'))
    
    return render_template('patient/profile.html', user=user)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'message': 'Healthcare Brain Tumor Detection System (Demo Mode)',
        'version': '1.0.0-demo'
    }

if __name__ == '__main__':
    print("\n" + "="*50)
    print("🧠 NeuroHealth - Brain Tumor Detection System")
    print("="*50)
    print("🐍 Python-Only Demo Version")
    print("🌐 Access: http://localhost:5000")
    print("\n🔑 Demo Login Credentials:")
    print("👨‍💼 Admin:   admin@healthcare.com / admin123")
    print("👨‍⚕️ Doctor:  doctor@healthcare.com / doctor123")
    print("🧑‍🦱 Patient: patient@healthcare.com / patient123")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)