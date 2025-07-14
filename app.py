from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
import os
from config import Config
from utils.db import db_instance

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize session
    Session(app)
    
    # Initialize database connection
    if not db_instance.connect():
        print("Failed to connect to database!")
        return None
    
    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.doctor import doctor_bp
    from routes.patient import patient_bp
    from routes.ml import ml_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(doctor_bp, url_prefix='/doctor')
    app.register_blueprint(patient_bp, url_prefix='/patient')
    app.register_blueprint(ml_bp, url_prefix='/ml')
    
    # Home route - redirect based on user type
    @app.route('/')
    def index():
        if 'user_id' in session:
            user_type = session.get('user_type')
            if user_type == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user_type == 'doctor':
                return redirect(url_for('doctor.dashboard'))
            elif user_type == 'patient':
                return redirect(url_for('patient.dashboard'))
        return redirect(url_for('auth.login'))
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return {
            'status': 'healthy',
            'message': 'Healthcare Brain Tumor Detection System is running',
            'version': '1.0.0'
        }
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500
    
    # Context processor to make current user available in all templates
    @app.context_processor
    def inject_user():
        from utils.auth_utils import get_current_user
        return dict(current_user=get_current_user())
    
    # Create default admin user if not exists
    create_default_admin()
    
    return app

def create_default_admin():
    """Create default admin user if not exists"""
    try:
        from models.user import User
        user_model = User()
        
        # Check if admin exists
        admin_email = 'admin@healthcare.com'
        existing_admin = user_model.find_user_by_email(admin_email)
        
        if not existing_admin:
            # Create default admin
            admin_data = {
                'email': admin_email,
                'password': 'admin123',  # Change this in production
                'user_type': 'admin',
                'first_name': 'System',
                'last_name': 'Administrator',
                'phone': '+1234567890'
            }
            
            admin_id = user_model.create_user(admin_data)
            if admin_id:
                print(f"Default admin created with email: {admin_email}")
                print("Default admin password: admin123 (Please change this!)")
            else:
                print("Failed to create default admin")
        else:
            print("Admin user already exists")
            
    except Exception as e:
        print(f"Error creating default admin: {e}")

def create_sample_data():
    """Create sample data for testing"""
    try:
        from models.user import User
        user_model = User()
        
        # Create sample doctor
        doctor_email = 'doctor@healthcare.com'
        existing_doctor = user_model.find_user_by_email(doctor_email)
        
        if not existing_doctor:
            doctor_data = {
                'email': doctor_email,
                'password': 'doctor123',
                'user_type': 'doctor',
                'first_name': 'Dr. John',
                'last_name': 'Smith',
                'phone': '+1234567891',
                'specialization': 'Neurology',
                'license_number': 'MD12345',
                'experience_years': 10,
                'available_time_slots': ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00']
            }
            
            doctor_id = user_model.create_user(doctor_data)
            if doctor_id:
                # Auto-approve the sample doctor
                user_model.approve_doctor(doctor_id)
                print(f"Sample doctor created: {doctor_email} / doctor123")
        
        # Create sample patient
        patient_email = 'patient@healthcare.com'
        existing_patient = user_model.find_user_by_email(patient_email)
        
        if not existing_patient:
            patient_data = {
                'email': patient_email,
                'password': 'patient123',
                'user_type': 'patient',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'phone': '+1234567892',
                'date_of_birth': '1990-01-01',
                'gender': 'Female'
            }
            
            patient_id = user_model.create_user(patient_data)
            if patient_id:
                print(f"Sample patient created: {patient_email} / patient123")
                
    except Exception as e:
        print(f"Error creating sample data: {e}")

if __name__ == '__main__':
    app = create_app()
    if app:
        # Create sample data for testing
        create_sample_data()
        
        print("\n" + "="*50)
        print("Healthcare Brain Tumor Detection System")
        print("="*50)
        print("Python-Only Flask Application")
        print("Access the system at: http://localhost:5000")
        print("\nDefault Login Credentials:")
        print("Admin:   admin@healthcare.com / admin123")
        print("Doctor:  doctor@healthcare.com / doctor123")
        print("Patient: patient@healthcare.com / patient123")
        print("="*50 + "\n")
        
        # Start the Flask development server
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    else:
        print("Failed to create application!")