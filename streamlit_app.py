import streamlit as st
from PyPDF2 import PdfReader
import docx
import requests

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() if page.extract_text() else ''
    return text

# Function to extract text from a DOCX
def extract_text_from_docx(doc_file):
    doc = docx.Document(doc_file)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

# Function to interact with Hugging Face API to answer questions based on document content
def answer_question_hf(text, question):
    api_key = st.secrets["huggingface_api_key"]  # Get Hugging Face API key securely
    model = "deepset/roberta-base-squad2"  # Q&A model from Hugging Face

    url = f"https://api-inference.huggingface.co/models/{model}"
    
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "inputs": {
            "question": question,
            "context": text
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        answer = response.json().get('answer', 'Sorry, I could not find an answer.')
    else:
        answer = f"Error: {response.status_code}, {response.text}"

    return answer

# Streamlit app
def main():
    st.title("Chat App with Document Support (Using Hugging Face)")

    st.write("Upload a PDF or DOCX file, then ask questions based on its content.")
    
    # Upload PDF or DOCX
    uploaded_file = st.file_uploader("Upload a PDF or DOCX file", type=['pdf', 'docx'])
    
    if uploaded_file is not None:
        # Extract text based on file type
        if uploaded_file.name.endswith('.pdf'):
            document_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith('.docx'):
            document_text = extract_text_from_docx(uploaded_file)
        
        st.write("Document uploaded successfully.")
        
        # Chat functionality
        st.write("Now you can ask questions related to the document.")
        
        question = st.text_input("Enter your question:")
        
        if question:
            # Answering the question based on document
            answer = answer_question_hf(document_text, question)
            st.write("Answer:", answer)

if __name__ == "__main__":
    main()
