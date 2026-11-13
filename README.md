# CloudVault – Cloud File Storage & Document Management System

## Project Overview

CloudVault is a cloud-based file storage and document management system developed using Python Flask and Supabase Storage.

It provides a simple web dashboard where an authenticated administrator can upload, organize, search, view, download and delete files stored in cloud storage.

The project was developed as part of a Cloud Computing Internship at Veda Technology.

## Live Application

**Live URL:** https://cloudvault-cloud-storage-system.onrender.com

**GitHub Repository:** https://github.com/apooja751/cloudvault-cloud-storage-system

## Features

- User-friendly and responsive dashboard.
- Admin login and logout functionality.
- Upload supported files to cloud storage.
- Organize files into three categories:
  - Documents
  - Images
  - Others
- Filter files by category.
- Search uploaded files by filename.
- View uploaded files in the dashboard.
- Download stored files.
- Delete uploaded files.
- File type validation.
- Maximum upload size of 10 MB.
- Secure cloud storage using a private Supabase Storage bucket.
- Deployment on Render.

## Technologies Used

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Cloud Storage | Supabase Storage |
| Authentication | Flask Session |
| Configuration | Python-dotenv |
| Web Server | Gunicorn |
| Deployment | Render |
| Version Control | Git and GitHub |

## Supported File Types

The application currently supports:

- PDF (`.pdf`)
- Word Documents (`.doc`, `.docx`)
- Text Files (`.txt`)
- Images (`.jpg`, `.jpeg`, `.png`)

**Maximum file size:** 10 MB per file.

## File Category Organization

CloudVault organizes uploaded files into three categories:

| Category | Purpose |
|---|---|
| Documents | Store documents and PDFs |
| Images | Store JPG and PNG images |
| Others | Store other supported file types |

Files are stored in category folders inside the Supabase Storage bucket.

Example:

```text
cloudvault-files/
│
├── Documents/
│   └── document.pdf
│
├── Images/
│   └── photo.jpg
│
└── Others/
    └── notes.txt
```

## Project Structure

```text
cloud-file-storage-system/
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── index.html
│   └── login.html
│
├── screenshots/
│
├── app.py
├── storage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── DEPLOYMENT.md
└── ARCHITECTURE.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/apooja751/cloudvault-cloud-storage-system.git
cd cloudvault-cloud-storage-system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Supabase Storage

1. Create a Supabase project.
2. Open the Supabase Storage section.
3. Create a private bucket named `cloudvault-files`.
4. Obtain your Supabase project URL and secret key.
5. Copy `.env.example` and create a local `.env` file.
6. Configure the required environment variables.

Required environment variables:

```ini
SUPABASE_URL=your_supabase_project_url
SUPABASE_SECRET_KEY=your_supabase_secret_key
SUPABASE_BUCKET_NAME=cloudvault-files

APP_SECRET_KEY=your_application_secret_key
APP_USERNAME=your_admin_username
APP_PASSWORD=your_admin_password
```

**Security:** Never upload your actual `.env` file or expose your Supabase secret key. The `.env` file is excluded through `.gitignore`.

### 6. Run the Application

```bash
python app.py
```

Open the browser and visit:

http://127.0.0.1:5000

Log in using the administrator credentials configured in your `.env` file.

## Cloud Storage Integration

CloudVault uses Supabase Storage as its cloud object storage service.

The application connects to a private bucket named `cloudvault-files` through the Supabase Python client.

The storage module (`storage.py`) handles:

- Uploading files.
- Listing stored files.
- Downloading files.
- Deleting files.
- Organizing files into category folders.

## Authentication and Security

The application includes a basic administrator login system using Flask sessions.

Security measures include:

- Login protection for the dashboard.
- Authentication checks for file operations.
- Environment variables for sensitive credentials.
- Private Supabase Storage bucket.
- File extension validation.
- File size restriction of 10 MB.
- Secure filename handling.

**Note:** This is an internship demonstration project with basic single-administrator authentication. It is not a production-grade multi-user authentication system.

## Deployment

CloudVault is deployed using Render.

**Deployment URL:**

https://cloudvault-cloud-storage-system.onrender.com

**Deployment Configuration:**

- Platform: Render
- Runtime: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Branch: `main`

The required environment variables are configured in the Render service settings.

For additional deployment instructions, refer to [DEPLOYMENT.md](DEPLOYMENT.md).

## Cloud Architecture

The application follows a simple cloud-based architecture:

1. The user accesses CloudVault through a web browser.
2. The Render web service hosts the Flask application.
3. Flask handles authentication and file operations.
4. The storage module communicates with Supabase Storage.
5. Files are stored in the private `cloudvault-files` bucket.
6. GitHub stores the source code and supports automatic deployment to Render.

For the architecture diagram, refer to [ARCHITECTURE.md](ARCHITECTURE.md).

## Screenshots

The `screenshots/` folder contains project evidence, including:

- CloudVault dashboard.
- File upload interface.
- Selected file information.
- Successful file upload.
- My Files dashboard.
- Supabase Storage bucket.
- Login page.
- Render deployment success.
- Render rollback evidence.
- Live category organization.
- Live category upload interface.

## Future Enhancements

- Multi-user authentication and role-based access control.
- Additional file formats.
- Folder creation and management.
- File sharing with access permissions.
- File previews.
- Improved cloud storage monitoring.

## Project Information

**Project Name:** CloudVault – Cloud File Storage & Document Management System

**Internship Domain:** Cloud Computing

**Organization:** Veda Technology

**Backend:** Python Flask

**Cloud Storage:** Supabase Storage

**Deployment Platform:** Render

**Source Code:** GitHub

---

Developed as part of the Veda Technology Cloud Computing Internship.