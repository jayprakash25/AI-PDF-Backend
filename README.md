# Fullstack Internship Assignment - Backend

## Overview

This repository contains the backend code for a full-stack application that allows users to upload PDF documents and ask questions regarding their content. The backend processes these documents and utilizes natural language processing to provide answers to the questions posed by the users.

## Tools and Technologies

- **Framework**: FastAPI
- **NLP Processing**: LangChain
- **Database**: PostgreSQL (for storing document metadata)
- **File Storage**:cloud storage (AWS S3) for storing uploaded PDFs

## Features

1. **PDF Upload**
   - Users can upload PDF documents.
   - The application stores the PDF and extracts its text content for processing.
   
2. **Asking Questions**
   - Users can ask questions related to the content of an uploaded PDF.
   - The system processes the question and the content of the PDF to provide an answer.
   
3. **Displaying Answers**
   - The application displays the answer to the user’s question.
   - User can ask follow-up or new questions on the same as well as different documents at a time.

### FastAPI Endpoints

- **POST /upload**
  - Endpoint for uploading PDF documents.
  
- **POST /question**
  - Endpoint for receiving questions and returning answers based on the uploaded PDFs.

## Setup Instructions

### Prerequisites

- Python 3.10
- PostgreSQL

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/fullstack-internship-backend.git
   cd fullstack-internship-backend

2. **Create and activate a virtual environment**:
     ```bash
     python -m venv env
     source env/bin/activate  # env\Scripts\activate --for windows


3. **Install dependencies**:
     ```bash
     pip install -r requirements.txt

4. **Run the application**:
     ```bash
     uvicorn app.main:app --reload

### Environment variables
  ```bash
OPENAI_API_KEY='YOUR OPENAI API KEY'
ACCESS_KEY='AWS ACCESS KEY'
SECRET_KEY='AWS SECRET KEY'
BUCKET_NAME='AWS S3 BUCKET NAME'
DATABASE_URL ='postgres://{user}:{password}@{hostname}:{port}/{database-name}' or hosted service url 



     
