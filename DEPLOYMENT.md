
# CloudVault Deployment Guide

## 1. Project Overview
CloudVault is a Flask-based cloud file storage and document management application.

## 2. Hosting Platform
- Hosting: Render
- Application: Flask
- Server: Gunicorn
- Cloud Storage: Supabase Storage
- Source Code: GitHub

## 3. Deployment Configuration

Build Command:
`pip install -r requirements.txt`

Start Command:
`gunicorn app:app`

Branch: `main`

## 4. Environment Variables

Configure these variables in the Render dashboard:

- SUPABASE_URL
- SUPABASE_SECRET_KEY
- SUPABASE_BUCKET_NAME
- APP_SECRET_KEY
- APP_USERNAME
- APP_PASSWORD

Actual secret values must never be committed to GitHub.

## 5. Deployment Steps

1. Push the project source code to GitHub.
2. Connect the GitHub repository to Render.
3. Configure the build and start commands.
4. Add the required environment variables.
5. Deploy the web service.
6. Test login, upload, listing, download and deletion.

## 6. Rollback Procedure

1. Open the CloudVault service in Render.
2. Open the Deploys page.
3. Select an earlier successful deployment.
4. Click Rollback.
5. Confirm the rollback.
6. Verify that the previous version is live.

## 7. Storage

Supabase Storage uses the private bucket `cloudvault-files` to store uploaded documents.
