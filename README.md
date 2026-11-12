# CloudVault – Cloud File Storage & Document Management System

## Project Overview

CloudVault is a cloud-based file storage and document management system developed using Python Flask and Supabase Storage. It allows users to upload, view, download, and delete documents through a simple web interface.

## Features

- User-friendly dashboard
- Upload multiple supported document types
- File type and size validation
- Store files securely in Supabase Storage
- View uploaded files
- Download stored documents
- Delete uploaded documents
- Search uploaded files
- Responsive web interface

## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Cloud Storage:** Supabase Storage
- **Configuration:** Python dotenv
- **Version Control:** Git and GitHub

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
│   └── index.html
│
├── screenshots/
├── app.py
├── storage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd cloud-file-storage-system
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Supabase

- Create a Supabase project.
- Create a private Storage bucket named `cloudvault-files`.
- Copy `.env.example` to a new file named `.env`.
- Add your own Supabase project URL and secret key to `.env`.

Never share or upload your actual `.env` file.

### 6. Run the application

```bash
python app.py
```

Open your browser and visit:

http://127.0.0.1:5000

## Storage Information

CloudVault uses Supabase Storage with a private bucket to store uploaded documents.

## Security Note

- Keep Supabase secret keys private.
- Never commit the `.env` file.
- The application is intended as an internship project and local demonstration. Authentication and production security enhancements are future improvements.

## Project Name

**CloudVault – Cloud File Storage & Document Management System**

Developed as part of a Cloud Computing Internship.
