from fastapi import APIRouter, File, UploadFile
from app.core import config
from app.services import question_process
from app.models import pdf
from app.core.database import SessionLocal
import datetime
from typing import List
import asyncio
import logging
import os
import psycopg2

router = APIRouter()

from app.api.endpoints import utils

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/upload/")
async def upload_pdf(files: List[UploadFile] = File(...)):
    try:
        # Extract text from the PDF
        text = await question_process.extract_text_from_pdf(files)
        logger.info(f"Extracted text: {text}")
        utils.combined_text += text

        # Split the text into chunks using LangChain's character splitter
        chunks = question_process.get_text_chunks(utils.combined_text)

        # Vectorize the text
        vector_store = question_process.get_vector_store(chunks)

        # Update the global variable with the new vector store
        utils.global_vector_store = vector_store

        # Connect to the PostgreSQL database
        DATABASE_URL = os.getenv("DATABASE_URL")
        conn = psycopg2.connect(DATABASE_URL)

        # Initialize a list to store any errors encountered
        upload_errors = []

        # Process each file
        for file in files:
            try:
                # Create a cursor object
                cur = conn.cursor()

                # Insert the PDF metadata into the database
                filename = file.filename
                upload_date = datetime.datetime.now()
                text = None  # Assuming you don't have the text content yet
                insert_query = "INSERT INTO pdfs (filename, upload_date, text) VALUES (%s, %s, %s)"
                cur.execute(insert_query, (filename, upload_date, text))

                # Commit the changes
                conn.commit()

                # Close the cursor
                cur.close()

                # Upload the file to S3
                await asyncio.to_thread(config.upload_to_s3, file.file, file.filename)
            except Exception as file_error:
                # Collect any errors encountered during file processing
                logger.error(f"Error processing file {file.filename}: {file_error}")
                upload_errors.append({"file": file.filename, "error": str(file_error)})

        # Close the database connection
        conn.close()

        if upload_errors:
            return {
                "status": "partial_success",
                "message": "Some files failed to upload",
                "errors": upload_errors
            }
        return {"status": "success", "message": "All files uploaded successfully"}
    except Exception as e:
        # General exception handler
        logger.error(f"General error: {str(e)}")
        return {"status": "failed", "message": str(e)}