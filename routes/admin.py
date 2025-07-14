from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.user import User
from models.appointment import Appointment
from models.prediction import Prediction
from utils.auth_utils import admin_required

admin_bp = Blueprint('admin', __name__)
user_model = User()
appointment_model = Appointment()
prediction_model = Prediction()

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard with system statistics"""
    try:
        # Get statistics
        all_doctors = user_model.get_all_doctors()
        approved_doctors = user_model.get_approved_doctors()
        
        total_doctors = len(all_doctors)
        total_approved_doctors = len(approved_doctors)
        total_pending_doctors = total_doctors - total_approved_doctors
        
        # Get prediction stats
        predictions_stats = prediction_model.get_predictions_stats()
        
        stats = {
            'total_doctors': total_doctors,
            'approved_doctors': total_approved_doctors,
            'pending_doctors': total_pending_doctors,
            'total_predictions': predictions_stats.get('total_predictions', 0),
            'reviewed_predictions': predictions_stats.get('reviewed_predictions', 0)
        }
        
        return render_template('admin/dashboard.html', stats=stats)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return render_template('admin/dashboard.html', stats={})

@admin_bp.route('/doctors')
@admin_required
def doctors():
    """Manage doctors page"""
    try:
        doctors = user_model.get_all_doctors()
        return render_template('admin/doctors.html', doctors=doctors)
    except Exception as e:
        flash(f'Error loading doctors: {str(e)}', 'error')
        return render_template('admin/doctors.html', doctors=[])

@admin_bp.route('/approve_doctor/<doctor_id>', methods=['POST'])
@admin_required
def approve_doctor(doctor_id):
    """Approve a doctor"""
    try:
        success = user_model.approve_doctor(doctor_id)
        if success:
            flash('Doctor approved successfully!', 'success')
        else:
            flash('Failed to approve doctor.', 'error')
    except Exception as e:
        flash(f'Error approving doctor: {str(e)}', 'error')
    
    return redirect(url_for('admin.doctors'))

@admin_bp.route('/patients')
@admin_required  
def patients():
    """View patients page"""
    # Simple implementation - would need to add patient list method
    return render_template('admin/patients.html', patients=[])

@admin_bp.route('/predictions')
@admin_required
def predictions():
    """View all predictions"""
    try:
        predictions = prediction_model.get_all_predictions()
        return render_template('admin/predictions.html', predictions=predictions)
    except Exception as e:
        flash(f'Error loading predictions: {str(e)}', 'error')
        return render_template('admin/predictions.html', predictions=[])

@admin_bp.route('/appointments')
@admin_required
def appointments():
    """View all appointments"""
    try:
        appointments = appointment_model.get_pending_appointments()
        return render_template('admin/appointments.html', appointments=appointments)
    except Exception as e:
        flash(f'Error loading appointments: {str(e)}', 'error')
        return render_template('admin/appointments.html', appointments=[])