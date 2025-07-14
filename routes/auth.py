from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from utils.auth_utils import login_user, logout_user, get_current_user
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)
user_model = User()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        
        if not email or not password or not user_type:
            flash('Please fill in all fields.', 'error')
            return render_template('auth/login.html')
        
        # Find user by email
        user = user_model.find_user_by_email(email)
        if not user:
            flash('Invalid email or password.', 'error')
            return render_template('auth/login.html')
        
        # Check user type
        if user['user_type'] != user_type:
            flash('Invalid user type selected.', 'error')
            return render_template('auth/login.html')
        
        # Verify password
        if not user_model.verify_password(password, user['password']):
            flash('Invalid email or password.', 'error')
            return render_template('auth/login.html')
        
        # Check if user is active
        if not user.get('is_active', True):
            flash('Your account has been deactivated.', 'error')
            return render_template('auth/login.html')
        
        # For doctors, check if approved by admin
        if user_type == 'doctor' and not user.get('approved_by_admin', False):
            flash('Your doctor account is pending admin approval.', 'warning')
            return render_template('auth/login.html')
        
        # Login successful
        login_user(user)
        flash(f'Welcome back, {user["first_name"]}!', 'success')
        
        # Redirect based on user type
        if user_type == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif user_type == 'doctor':
            return redirect(url_for('doctor.dashboard'))
        elif user_type == 'patient':
            return redirect(url_for('patient.dashboard'))
    
    return render_template('auth/login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page for patients only"""
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        
        # Validation
        if not all([email, password, confirm_password, first_name, last_name, phone]):
            flash('Please fill in all required fields.', 'error')
            return render_template('auth/signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('auth/signup.html')
        
        # Check if user already exists
        existing_user = user_model.find_user_by_email(email)
        if existing_user:
            flash('An account with this email already exists.', 'error')
            return render_template('auth/signup.html')
        
        # Create patient user
        user_data = {
            'email': email,
            'password': password,
            'user_type': 'patient',
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'date_of_birth': date_of_birth,
            'gender': gender
        }
        
        user_id = user_model.create_user(user_data)
        if user_id:
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Failed to create account. Please try again.', 'error')
    
    return render_template('auth/signup.html')

@auth_bp.route('/logout')
def logout():
    """Logout and redirect to login page"""
    user_name = session.get('user_name', 'User')
    logout_user()
    flash(f'Goodbye, {user_name}!', 'info')
    return redirect(url_for('auth.login'))