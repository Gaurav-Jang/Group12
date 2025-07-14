from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.appointment import Appointment
from models.prediction import Prediction
from utils.auth_utils import doctor_required, get_current_user

doctor_bp = Blueprint('doctor', __name__)
appointment_model = Appointment()
prediction_model = Prediction()

@doctor_bp.route('/dashboard')
@doctor_required
def dashboard():
    """Doctor dashboard"""
    current_user = get_current_user()
    try:
        # Get doctor's appointments and predictions
        appointments = appointment_model.get_doctor_appointments(current_user['_id'])
        predictions = prediction_model.get_doctor_predictions(current_user['_id'])
        
        stats = {
            'total_appointments': len(appointments),
            'pending_appointments': len([a for a in appointments if a.get('status') == 'pending']),
            'total_predictions': len(predictions),
            'pending_reviews': len([p for p in predictions if not p.get('reviewed_by_doctor', False)])
        }
        
        return render_template('doctor/dashboard.html', stats=stats, recent_appointments=appointments[:5])
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('doctor/dashboard.html', stats={}, recent_appointments=[])

@doctor_bp.route('/appointments')
@doctor_required
def appointments():
    """Doctor appointments management"""
    current_user = get_current_user()
    try:
        appointments = appointment_model.get_doctor_appointments(current_user['_id'])
        return render_template('doctor/appointments.html', appointments=appointments)
    except Exception as e:
        flash(f'Error loading appointments: {str(e)}', 'error')
        return render_template('doctor/appointments.html', appointments=[])

@doctor_bp.route('/predictions')
@doctor_required
def predictions():
    """Doctor predictions review"""
    current_user = get_current_user()
    try:
        predictions = prediction_model.get_doctor_predictions(current_user['_id'])
        return render_template('doctor/predictions.html', predictions=predictions)
    except Exception as e:
        flash(f'Error loading predictions: {str(e)}', 'error')
        return render_template('doctor/predictions.html', predictions=[])

@doctor_bp.route('/schedule')
@doctor_required
def schedule():
    """Doctor schedule management"""
    return render_template('doctor/schedule.html')