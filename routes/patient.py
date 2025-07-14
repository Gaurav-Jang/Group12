from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.appointment import Appointment
from models.prediction import Prediction
from models.user import User
from utils.auth_utils import patient_required, get_current_user

patient_bp = Blueprint('patient', __name__)
appointment_model = Appointment()
prediction_model = Prediction()
user_model = User()

@patient_bp.route('/dashboard')
@patient_required
def dashboard():
    """Patient dashboard"""
    current_user = get_current_user()
    try:
        # Get patient's appointments and predictions
        appointments = appointment_model.get_patient_appointments(current_user['_id'])
        predictions = prediction_model.get_patient_predictions(current_user['_id'])
        
        stats = {
            'total_appointments': len(appointments),
            'upcoming_appointments': len([a for a in appointments if a.get('status') == 'approved']),
            'total_scans': len(predictions),
            'recent_scans': len([p for p in predictions if p.get('status') == 'pending_review'])
        }
        
        return render_template('patient/dashboard.html', stats=stats, recent_appointments=appointments[:3])
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('patient/dashboard.html', stats={}, recent_appointments=[])

@patient_bp.route('/tumor_detection')
@patient_required
def tumor_detection():
    """MRI scan upload and analysis page"""
    return render_template('patient/tumor_detection.html')

@patient_bp.route('/appointments')
@patient_required
def appointments():
    """Patient appointment booking and management"""
    current_user = get_current_user()
    try:
        appointments = appointment_model.get_patient_appointments(current_user['_id'])
        doctors = user_model.get_approved_doctors()
        return render_template('patient/appointments.html', appointments=appointments, doctors=doctors)
    except Exception as e:
        flash(f'Error loading appointments: {str(e)}', 'error')
        return render_template('patient/appointments.html', appointments=[], doctors=[])

@patient_bp.route('/results')
@patient_required
def results():
    """Patient scan results and predictions"""
    current_user = get_current_user()
    try:
        predictions = prediction_model.get_patient_predictions(current_user['_id'])
        return render_template('patient/results.html', predictions=predictions)
    except Exception as e:
        flash(f'Error loading results: {str(e)}', 'error')
        return render_template('patient/results.html', predictions=[])

@patient_bp.route('/profile')
@patient_required
def profile():
    """Patient profile management"""
    current_user = get_current_user()
    return render_template('patient/profile.html', user=current_user)