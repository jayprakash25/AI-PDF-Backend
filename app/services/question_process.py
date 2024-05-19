import os
import boto3
import fitz
import io
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

# Set-up AWS S3 Client
s3 = boto3.client('s3',
                  region_name='ap-south-2',
                  aws_access_key_id=os.getenv('ACCESS_KEY'),
                  aws_secret_access_key=os.getenv('SECRET_KEY'))

# Function to load the pdf from S3 and extract text
def load_pdf_from_s3(s3_key: str, bucket_name: str) -> str:
    obj = s3.get_object(Bucket=bucket_name, Key=s3_key)
    pdf = obj['Body'].read()

    # Extract text from the pdf
    doc = fitz.open(stream=pdf, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    return text

# Function to extract text from pdf
async def extract_text_from_pdf(pdfs):
    text = ""
    for pdf in pdfs:
        # Read the file into a bytes object
        pdf_bytes = await pdf.read()

        # Create a BytesIO object 
        pdf_io = io.BytesIO(pdf_bytes)

        # Create a PdfReader object
        pdf_reader = PdfReader(pdf_io)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
    chunks = text_splitter.split_text(text)
    
    return chunks

# Function to generate vector store from chunks
def get_vector_store(chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=chunks, embedding=embeddings)

    return vectorstore

# Function to create a conversation chain
def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vectorstore.as_retriever(),
        memory = memory
    )

    return conversation_chain

# Function to handle a question and generate a response
def handle_question(question, conversation_chain):
    response = conversation_chain.run(question)
    return response