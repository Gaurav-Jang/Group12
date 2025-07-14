from functools import wraps
from flask import session, request, redirect, url_for, flash
from models.user import User

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        
        user_model = User()
        user = user_model.find_user_by_id(session['user_id'])
        
        if not user or user.get('user_type') != 'admin':
            flash('Admin privileges required.', 'error')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

def doctor_required(f):
    """Decorator to require doctor privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        
        user_model = User()
        user = user_model.find_user_by_id(session['user_id'])
        
        if not user or user.get('user_type') not in ['admin', 'doctor']:
            flash('Doctor privileges required.', 'error')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

def patient_required(f):
    """Decorator to require patient privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        
        user_model = User()
        user = user_model.find_user_by_id(session['user_id'])
        
        if not user or user.get('user_type') not in ['admin', 'patient']:
            flash('Patient privileges required.', 'error')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current user from session"""
    if 'user_id' in session:
        user_model = User()
        return user_model.find_user_by_id(session['user_id'])
    return None

def login_user(user):
    """Log in a user by setting session variables"""
    session['user_id'] = str(user['_id'])
    session['user_type'] = user['user_type']
    session['user_name'] = f"{user['first_name']} {user['last_name']}"
    session['user_email'] = user['email']

def logout_user():
    """Log out the current user by clearing session"""
    session.clear()

def is_logged_in():
    """Check if user is logged in"""
    return 'user_id' in session