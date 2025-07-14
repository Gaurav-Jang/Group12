# Healthcare Brain Tumor Detection System - Python Only

## Project Structure
```
/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
├── models/
│   ├── __init__.py
│   ├── user.py                 # User models (Admin, Doctor, Patient)
│   ├── appointment.py          # Appointment model
│   └── prediction.py           # ML prediction model
├── routes/
│   ├── __init__.py
│   ├── auth.py                 # Authentication routes
│   ├── admin.py                # Admin routes
│   ├── doctor.py               # Doctor routes
│   ├── patient.py              # Patient routes
│   └── ml.py                   # ML prediction routes
├── utils/
│   ├── __init__.py
│   ├── db.py                   # MongoDB connection
│   ├── auth_utils.py           # Authentication utilities
│   └── ml_model.py             # Brain tumor detection model
├── templates/
│   ├── base.html               # Base template
│   ├── auth/
│   │   ├── login.html          # Login page
│   │   └── signup.html         # Patient signup
│   ├── admin/
│   │   ├── dashboard.html      # Admin dashboard
│   │   ├── doctors.html        # Manage doctors
│   │   └── patients.html       # View patients
│   ├── doctor/
│   │   ├── dashboard.html      # Doctor dashboard
│   │   ├── appointments.html   # Manage appointments
│   │   └── predictions.html    # Review predictions
│   ├── patient/
│   │   ├── dashboard.html      # Patient dashboard
│   │   ├── tumor_detection.html # Upload MRI scans
│   │   ├── appointments.html   # Book appointments
│   │   └── results.html        # View results
│   └── components/
│       ├── navbar.html         # Navigation bar
│       ├── sidebar.html        # Sidebar navigation
│       └── footer.html         # Footer
├── static/
│   ├── css/
│   │   ├── style.css           # Custom styles
│   │   └── bootstrap.min.css   # Bootstrap CSS
│   ├── js/
│   │   ├── main.js             # Main JavaScript
│   │   └── bootstrap.min.js    # Bootstrap JS
│   ├── images/
│   │   └── favicon.ico         # Favicon
│   └── uploads/
│       └── mri_images/         # Uploaded MRI images
├── ml_models/
│   └── brain_tumor_model.h5    # Trained model
└── README.md
```

## Features (All Preserved)
- Admin panel for doctor management
- Patient registration and appointment booking  
- Doctor login and appointment approval
- Brain tumor detection from MRI images
- Time slot management for appointments
- Secure authentication system
- Modern responsive UI with Bootstrap
- File upload and processing
- Role-based access control