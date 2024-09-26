import streamlit as st
from PyPDF2 import PdfReader
import docx
import openai

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from a DOCX
def extract_text_from_docx(doc_file):
    doc = docx.Document(doc_file)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text

# Function to interact with OpenAI API to answer questions based on document content
def answer_question(text, question):
    openai.api_key = st.secrets["openai_api_key"]  # Fetch the OpenAI API key securely
    prompt = f"Given the following document: {text}\nAnswer the question: {question}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",  # or "gpt-3.5-turbo"
        prompt=prompt,
        max_tokens=500,
        temperature=0.5
    )
    
    answer = response.choices[0].text.strip()
    return answer

# Streamlit app
def main():
    st.title("Chat App with Document Support")

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
            answer = answer_question(document_text, question)
            st.write("Answer:", answer)

if __name__ == "__main__":
    main()
