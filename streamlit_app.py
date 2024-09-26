import streamlit as st
from PyPDF2 import PdfReader
import docx
from langchain import OpenAI
from langchain.prompts import PromptTemplate

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

# Function to answer user questions based on document content
def answer_question(text, question):
    # Using a simple LLM like OpenAI for Q&A
    llm = OpenAI(model="gpt-3.5-turbo")
    prompt_template = PromptTemplate(
        input_variables=["text", "question"],
        template="Given the following document: {text}, answer the question: {question}"
    )
    prompt = prompt_template.format(text=text, question=question)
    return llm(prompt)

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
