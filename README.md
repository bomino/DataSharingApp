# Data Collection Manager

A Django-based web application for managing and sharing data files with role-based access control.

## Features

### User Management
- Role-based access control (Admin, Analyst, Basic User)
- Secure authentication system
- Custom user profiles

### File Management
- Upload data files (CSV, XLSX, XLS)
- Automatic file validation
- Version control
- File organization by user and date
- Maximum file size: 10MB

### File Sharing
- Share files with specific users
- Automatic 7-day expiration for shared files
- Track shared file status
- Manage file access permissions

### Dashboard
- Overview of file statistics
- Recent activity tracking
- File validation status
- Sharing metrics

## Technical Requirements

- Python 3.11+
- Django 5.1+
- Additional packages listed in requirements.txt

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd data_collection_project
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Project Structure
```
data_collection_project/
├── data_manager/                 # Main application
│   ├── migrations/              # Database migrations
│   ├── templates/               # HTML templates
│   │   ├── data_manager/       # App-specific templates
│   │   └── registration/       # Auth templates
│   ├── static/                 # Static files
│   │   ├── css/               # Stylesheets
│   │   ├── js/                # JavaScript files
│   │   └── images/            # Image assets
│   ├── models.py              # Database models
│   ├── views.py               # View logic
│   ├── urls.py                # URL routing
│   └── forms.py               # Form definitions
└── static/                    # Project-level static files
```

## User Roles

### Admin
- Full access to all features
- Can manage users
- Can view all files
- Can share files

### Analyst
- Can upload and manage own files
- Can share files
- Can view sharing statistics

### Basic User
- Can upload files
- Can view own files
- Cannot share files

## API Endpoints

- `/api/files/` - File management endpoints
- `/api/token/` - JWT token generation
- `/api/token/refresh/` - JWT token refresh

## File Requirements

- Supported formats: CSV, XLSX, XLS
- Required columns: date, value, category
- Maximum file size: 10MB
- Files are automatically validated upon upload

## Security Features

- JWT authentication for API
- Role-based access control
- Secure file handling
- Automatic file expiration
- Session management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your License Information]

## Support

[Contact Information or Support Instructions]