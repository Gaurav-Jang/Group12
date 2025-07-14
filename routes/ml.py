from flask import Blueprint, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
from models.prediction import Prediction
from utils.auth_utils import login_required, get_current_user
from utils.ml_model import brain_tumor_detector
from config import Config

ml_bp = Blueprint('ml', __name__)
prediction_model = Prediction()

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@ml_bp.route('/predict', methods=['POST'])
@login_required
def predict():
    """Handle MRI image upload and prediction"""
    current_user = get_current_user()
    
    try:
        # Check if file was uploaded
        if 'mri_image' not in request.files:
            flash('No file uploaded.', 'error')
            return redirect(url_for('patient.tumor_detection'))
        
        file = request.files['mri_image']
        
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(url_for('patient.tumor_detection'))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload an image file.', 'error')
            return redirect(url_for('patient.tumor_detection'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = str(int(os.path.getmtime(__file__) * 1000))
        unique_filename = f"{timestamp}_{filename}"
        
        # Ensure upload directory exists
        upload_path = os.path.join(Config.UPLOAD_FOLDER)
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        # Make prediction
        prediction_result = brain_tumor_detector.predict(file_path)
        
        if prediction_result is None:
            flash('Error analyzing the image. Please try again.', 'error')
            return redirect(url_for('patient.tumor_detection'))
        
        # Save prediction to database
        prediction_data = {
            'patient_id': str(current_user['_id']),
            'image_path': file_path,
            'image_name': filename,
            'prediction_result': prediction_result['result'],
            'confidence_score': prediction_result['confidence'],
            'model_version': prediction_result['model_version'],
            'prediction_details': {
                'tumor_probability': prediction_result.get('tumor_probability', 0),
                'no_tumor_probability': prediction_result.get('no_tumor_probability', 0)
            }
        }
        
        prediction_id = prediction_model.create_prediction(prediction_data)
        
        if prediction_id:
            result_text = "Tumor detected" if prediction_result['result'] == 'tumor_detected' else "No tumor detected"
            confidence_text = f"{prediction_result['confidence']:.1%}"
            
            flash(f'Analysis complete: {result_text} (Confidence: {confidence_text})', 'success')
        else:
            flash('Error saving prediction results.', 'error')
        
        return redirect(url_for('patient.results'))
        
    except Exception as e:
        flash(f'Error processing image: {str(e)}', 'error')
        return redirect(url_for('patient.tumor_detection'))

@ml_bp.route('/prediction/<prediction_id>')
@login_required
def get_prediction(prediction_id):
    """Get specific prediction details"""
    try:
        prediction = prediction_model.get_prediction_by_id(prediction_id)
        if prediction:
            return jsonify({
                'success': True,
                'prediction': {
                    'id': str(prediction['_id']),
                    'result': prediction['prediction_result'],
                    'confidence': prediction['confidence_score'],
                    'created_at': prediction['created_at'].isoformat(),
                    'image_name': prediction['image_name']
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Prediction not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500