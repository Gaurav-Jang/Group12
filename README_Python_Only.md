# 🧠 NeuroHealth - Python-Only Healthcare System

## 🌟 **Brain Tumor Detection System with Flask**

A comprehensive healthcare application built entirely in **Python** using Flask for brain tumor detection from MRI images with MongoDB backend and machine learning integration.

---

## 🚀 **Features**

### 🔐 **Multi-Role Authentication System**
- **Admin Panel**: Doctor management, system oversight
- **Doctor Portal**: Appointment management, prediction review
- **Patient Portal**: MRI upload, appointment booking, results viewing

### 🧠 **AI-Powered Brain Tumor Detection**
- CNN-based tumor detection from MRI images
- Real-time image analysis and prediction
- Confidence scoring and region analysis
- Medical image preprocessing and enhancement

### 📅 **Appointment Management**
- Patient-doctor appointment booking
- Time slot management and availability
- Appointment approval workflow
- Automated conflict prevention

### 📊 **Comprehensive Dashboard**
- Real-time statistics and analytics
- User activity monitoring
- System health indicators
- Role-specific data visualization

---

## 🛠 **Technology Stack**

### **Backend Framework**
- **Flask 2.3.2** - Web application framework
- **Jinja2** - Server-side templating
- **Flask-WTF** - Form handling and CSRF protection
- **Flask-Session** - Session management

### **Database**
- **MongoDB** - Document database for flexible data storage
- **PyMongo** - MongoDB driver for Python

### **Machine Learning**
- **TensorFlow 2.13.0** - Deep learning framework
- **OpenCV** - Computer vision and image processing
- **NumPy** - Numerical computing
- **Pillow** - Image processing library

### **Frontend**
- **Bootstrap 5.3** - Responsive UI framework
- **Font Awesome 6.4** - Icon library
- **Vanilla JavaScript** - Client-side interactions

### **Security**
- **bcrypt** - Password hashing
- **Session-based authentication** - Secure user sessions
- **CSRF protection** - Form security

---

## 📋 **Prerequisites**

### **System Requirements**
- Python 3.8 or higher
- MongoDB 4.4 or higher
- 4GB RAM minimum (8GB recommended for ML operations)
- 2GB free disk space

### **Required Software**
```bash
# Install MongoDB (Ubuntu/Debian)
sudo apt update
sudo apt install -y mongodb

# Install MongoDB (macOS with Homebrew)
brew tap mongodb/brew
brew install mongodb-community

# Install MongoDB (Windows)
# Download from: https://www.mongodb.com/try/download/community
```

---

## 🔧 **Installation & Setup**

### **1. Clone and Setup Project**
```bash
# Clone the repository (or extract files)
cd /workspace

# Create virtual environment
python -m venv healthcare_env

# Activate virtual environment
# On Linux/macOS:
source healthcare_env/bin/activate
# On Windows:
healthcare_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Database Configuration**
```bash
# Start MongoDB service
# On Linux:
sudo systemctl start mongod
sudo systemctl enable mongod

# On macOS:
brew services start mongodb/brew/mongodb-community

# On Windows:
net start MongoDB
```

### **3. Environment Setup**
```bash
# The .env file is already configured with default values
# You can modify MongoDB URI and other settings if needed
# Default MongoDB URI: mongodb://localhost:27017/
```

### **4. Initialize Application**
```bash
# Create necessary directories
mkdir -p static/uploads/mri_images
mkdir -p ml_models

# Run the application
python app.py
```

---

## 🚦 **Running the Application**

### **Start the System**
```bash
# Activate virtual environment (if not already active)
source healthcare_env/bin/activate  # Linux/macOS
# or
healthcare_env\Scripts\activate     # Windows

# Start the Flask application
python app.py
```

### **Access the Application**
- **URL**: http://localhost:5000
- The application will automatically create default users on first run

---

## 👥 **Default User Accounts**

### **Administrator**
```
Email: admin@healthcare.com
Password: admin123
Role: System Administrator
```

### **Doctor** 
```
Email: doctor@healthcare.com
Password: doctor123
Role: Neurologist (Pre-approved)
```

### **Patient**
```
Email: patient@healthcare.com
Password: patient123
Role: Patient Account
```

---

## 📖 **User Guide**

### **For Patients**
1. **Signup/Login**: Create account or login at http://localhost:5000
2. **Upload MRI**: Navigate to "Brain Scan Analysis" to upload MRI images
3. **Book Appointments**: Use "Book Appointment" to schedule with doctors
4. **View Results**: Check "My Results" for scan analysis and medical reports
5. **Manage Profile**: Update personal information in "My Profile"

### **For Doctors**
1. **Login**: Use doctor credentials at http://localhost:5000
2. **Dashboard**: View appointment summary and pending predictions
3. **Appointments**: Approve/reject patient appointment requests
4. **Review Predictions**: Analyze AI predictions and add medical notes
5. **Schedule**: Manage availability and time slots

### **For Administrators**
1. **Login**: Use admin credentials at http://localhost:5000
2. **Dashboard**: Monitor system statistics and health
3. **Manage Doctors**: Approve new doctor registrations
4. **View Data**: Monitor predictions, appointments, and users
5. **System Health**: Check database and ML model status

---

## 🔌 **API Endpoints**

### **Authentication**
- `GET /auth/login` - Login page
- `POST /auth/login` - Process login
- `GET /auth/signup` - Patient signup page
- `POST /auth/signup` - Process signup
- `GET /auth/logout` - Logout user

### **Admin Routes**
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/doctors` - Manage doctors
- `POST /admin/approve_doctor/<id>` - Approve doctor
- `GET /admin/predictions` - View all predictions
- `GET /admin/appointments` - View all appointments

### **Doctor Routes**
- `GET /doctor/dashboard` - Doctor dashboard
- `GET /doctor/appointments` - Manage appointments
- `GET /doctor/predictions` - Review predictions
- `GET /doctor/schedule` - Manage schedule

### **Patient Routes**
- `GET /patient/dashboard` - Patient dashboard
- `GET /patient/tumor_detection` - MRI upload page
- `GET /patient/appointments` - Book appointments
- `GET /patient/results` - View results
- `GET /patient/profile` - Manage profile

### **ML Routes**
- `POST /ml/predict` - Upload and analyze MRI
- `GET /ml/prediction/<id>` - Get prediction details

---

## 🗂 **Project Structure**

```
healthcare-python-only/
├── app.py                    # Main Flask application
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
│
├── models/                   # Database models
│   ├── user.py              # User management
│   ├── appointment.py       # Appointment handling
│   └── prediction.py        # ML prediction storage
│
├── routes/                   # Flask blueprints
│   ├── auth.py              # Authentication routes
│   ├── admin.py             # Admin functionality
│   ├── doctor.py            # Doctor portal
│   ├── patient.py           # Patient portal
│   └── ml.py                # ML prediction handling
│
├── utils/                    # Utility modules
│   ├── db.py                # Database connection
│   ├── auth_utils.py        # Authentication helpers
│   └── ml_model.py          # Brain tumor detection model
│
├── templates/                # Jinja2 HTML templates
│   ├── base.html            # Base template
│   ├── components/          # Reusable components
│   ├── auth/                # Authentication pages
│   ├── admin/               # Admin templates
│   ├── doctor/              # Doctor templates
│   └── patient/             # Patient templates
│
├── static/                   # Static assets
│   ├── css/                 # Custom styles
│   ├── js/                  # JavaScript files
│   ├── images/              # Image assets
│   └── uploads/             # User uploads
│
└── ml_models/               # ML model files
    └── brain_tumor_model.h5 # Trained model (auto-created)
```

---

## 🤖 **Machine Learning Model**

### **Architecture**
- **Model Type**: Convolutional Neural Network (CNN)
- **Input**: 224x224x3 RGB images
- **Layers**: Conv2D, BatchNormalization, MaxPooling2D, Dense
- **Output**: Binary classification (Tumor/No Tumor)
- **Framework**: TensorFlow/Keras

### **Preprocessing**
- Image resizing to 224x224 pixels
- RGB conversion and normalization
- Data augmentation for training
- Real-time preprocessing pipeline

### **Prediction Process**
1. Image upload and validation
2. Preprocessing and resizing
3. Model inference
4. Confidence calculation
5. Result storage in database
6. Region analysis (optional)

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **MongoDB Connection Error**
```bash
# Check if MongoDB is running
sudo systemctl status mongod  # Linux
brew services list | grep mongodb  # macOS

# Start MongoDB if not running
sudo systemctl start mongod  # Linux
brew services start mongodb-community  # macOS
```

#### **Permission Denied (Upload Directory)**
```bash
# Fix upload directory permissions
chmod 755 static/uploads/mri_images
sudo chown -R $USER:$USER static/uploads/
```

#### **TensorFlow Installation Issues**
```bash
# For CPU-only version
pip uninstall tensorflow
pip install tensorflow-cpu

# For specific Python version
pip install tensorflow==2.13.0 --python-version=3.9
```

#### **Memory Issues with ML Model**
```python
# In utils/ml_model.py, reduce model complexity or batch size
# Add memory management:
import tensorflow as tf
tf.config.experimental.set_memory_growth(gpu_device, True)
```

---

## 🔒 **Security Considerations**

### **Production Deployment**
1. **Change Default Passwords**: Update all default credentials
2. **Environment Variables**: Use secure random values for SECRET_KEY
3. **Database Security**: Enable MongoDB authentication
4. **HTTPS**: Use SSL/TLS certificates
5. **File Upload**: Implement virus scanning and file validation
6. **Rate Limiting**: Add request rate limiting
7. **Session Security**: Configure secure session settings

### **Recommended Production Settings**
```python
# config.py - Production settings
SECRET_KEY = os.getenv('SECRET_KEY')  # 64-character random string
DEBUG = False
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
```

---

## 📈 **Performance Optimization**

### **Database Optimization**
```javascript
// MongoDB indexes for better performance
db.users.createIndex({"email": 1})
db.appointments.createIndex({"doctor_id": 1, "appointment_date": 1})
db.predictions.createIndex({"patient_id": 1, "created_at": -1})
```

### **ML Model Optimization**
- Use model quantization for faster inference
- Implement caching for frequent predictions
- Consider GPU acceleration for large-scale deployment
- Optimize image preprocessing pipeline

---

## 🔮 **Future Enhancements**

### **Technical Improvements**
- [ ] Real-time notifications with WebSockets
- [ ] Advanced ML models (ResNet, EfficientNet)
- [ ] Multi-language support (i18n)
- [ ] PDF report generation
- [ ] Email notifications
- [ ] Mobile app development

### **Medical Features**
- [ ] DICOM image support
- [ ] 3D brain visualization
- [ ] Multiple tumor type detection
- [ ] Treatment recommendation system
- [ ] Medical history tracking
- [ ] Integration with hospital systems

---

## 🆘 **Support & Contributing**

### **Getting Help**
- Check the troubleshooting section above
- Review MongoDB and Flask documentation
- Verify Python and dependency versions

### **Development**
- Follow PEP 8 style guidelines
- Add comprehensive tests
- Document new features
- Use type hints where applicable

---

## 📄 **License**

This is a demonstration healthcare system for educational purposes. For production use in medical environments, ensure compliance with:
- HIPAA (Health Insurance Portability and Accountability Act)
- GDPR (General Data Protection Regulation)
- Local medical data protection laws
- FDA regulations for medical software

---

## 🙏 **Acknowledgments**

- **Flask Community** for the excellent web framework
- **MongoDB** for flexible document storage
- **TensorFlow** for machine learning capabilities
- **Bootstrap** for responsive UI components
- **Open Source Community** for various libraries and tools

---

**📞 For technical support or questions about the Python-only implementation, please refer to the troubleshooting section or check the application logs for detailed error messages.**