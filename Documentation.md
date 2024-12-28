# Data Collection Manager Documentation

## Table of Contents
1. [System Overview](#1-system-overview)
2. [User Guide](#2-user-guide)
3. [Technical Documentation](#3-technical-documentation)
4. [API Documentation](#4-api-documentation)
5. [Security](#5-security)
6. [Troubleshooting](#6-troubleshooting)

## 1. System Overview

### 1.1 Purpose
The Data Collection Manager is a web-based application designed to facilitate secure file management and sharing within organizations. It provides role-based access control, file validation, and temporary file sharing capabilities.

### 1.2 System Architecture
- Django-based web application
- SQLite database (configurable for other databases)
- REST API with JWT authentication
- Bootstrap-based responsive frontend

### 1.3 Core Features
- User role management
- File upload and validation
- File sharing with expiration
- Analytics dashboard
- REST API access

## 2. User Guide

### 2.1 User Roles
#### Administrator
- Full system access
- User management
- Access to all files
- File sharing capabilities
- System statistics

#### Analyst
- File upload and management
- File sharing capabilities
- Access to sharing statistics
- API access

#### Basic User
- File upload capabilities
- Access to own files
- Cannot share files

### 2.2 File Management
#### Upload Process
1. Navigate to Upload page
2. Select file (CSV, XLSX, XLS)
3. File requirements:
   - Maximum size: 10MB
   - Required columns: date, value, category
4. Automatic validation occurs
5. Version control is applied

#### File Organization
- Files are organized by:
  - User
  - Upload date
  - Version number
- Naming convention: `username/YYYY-MM-DD/filename_v{version}.ext`

### 2.3 File Sharing
#### How to Share Files
1. Navigate to Shared Files
2. Click "Share File"
3. Select:
   - File to share
   - User to share with
4. Share expires after 7 days
5. Can unshare at any time

#### Managing Shared Files
- View active shares
- Monitor expiration dates
- Revoke access when needed
- Track sharing statistics

### 2.4 Dashboard
#### Available Statistics
- Total files count
- File validation status
- Recent uploads
- Active shares
- Expiring shares
- Recent sharing activity

## 3. Technical Documentation

### 3.1 Installation
#### Prerequisites
- Python 3.11+
- pip
- virtualenv

#### Setup Process
```bash
# Clone repository
git clone [repository-url]
cd data_collection_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### 3.2 Project Structure
```
data_collection_project/
├── data_manager/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
└── static/
```

### 3.3 Database Schema
#### User Model
```python
class User(AbstractUser):
    role = models.CharField(choices=[
        ('basic', 'Basic User'),
        ('analyst', 'Data Analyst'),
        ('admin', 'Administrator')
    ])
```

#### DataFile Model
```python
class DataFile(models.Model):
    file = models.FileField()
    uploaded_by = models.ForeignKey(User)
    version = models.PositiveIntegerField()
    validated = models.BooleanField()
```

#### SharedFile Model
```python
class SharedFile(models.Model):
    file = models.ForeignKey(DataFile)
    shared_by = models.ForeignKey(User)
    shared_with = models.ForeignKey(User)
    expiry_date = models.DateTimeField()
```

## 4. API Documentation

### 4.1 Authentication
```bash
# Get token
POST /api/token/
{
    "username": "user",
    "password": "pass"
}

# Refresh token
POST /api/token/refresh/
{
    "refresh": "token"
}
```

### 4.2 File Endpoints
#### List Files
```bash
GET /api/files/
Authorization: Bearer <token>
```

#### Upload File
```bash
POST /api/files/
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

#### File Detail
```bash
GET /api/files/{id}/
Authorization: Bearer <token>
```

### 4.3 Response Formats
```json
{
    "id": 1,
    "file": "url",
    "uploaded_at": "timestamp",
    "validated": boolean,
    "version": integer
}
```

## 5. Security

### 5.1 Authentication
- Django's authentication system
- JWT for API access
- Session management

### 5.2 File Security
- Validated file uploads
- Controlled access
- Automatic expiration
- Secure file storage

### 5.3 Access Control
- Role-based permissions
- File ownership tracking
- Share management
- API access control

## 6. Troubleshooting

### 6.1 Common Issues
#### File Upload Failures
- Check file size (max 10MB)
- Verify file format
- Confirm required columns
- Check permissions

#### Sharing Issues
- Verify user roles
- Check expiration dates
- Confirm file permissions
- Check share status

### 6.2 Error Messages
- Detailed error descriptions
- Common solutions
- Contact information

### 6.3 Support
For additional support:
- Contact system administrator
- Check error logs
- Review documentation
- Submit bug reports