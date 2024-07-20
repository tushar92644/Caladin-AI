import os  # Importing os module for operating system dependent functionality
import time  # Importing time module to use time-related functions
from PyPDF2 import PdfReader  # Importing PdfReader from PyPDF2 to read PDF files
import streamlit as st  # Importing streamlit for web app development
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Importing RecursiveCharacterTextSplitter for text splitting
from langchain_google_genai import GoogleGenerativeAIEmbeddings  # Importing GoogleGenerativeAIEmbeddings for embeddings
import google.generativeai as genai  # Importing generative AI library
from langchain_community.vectorstores import FAISS  # Importing FAISS vector store
from prompt import construct_prompt  # Importing custom prompt construction
import base64  # Importing base64 for encoding files

# Load environment variables for Google API key
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)  # Configure generative AI with the API key

# Function to extract text from PDF
def get_pdf_text(pdf_path):
    pdf_reader = PdfReader(pdf_path)  # Initialize PDF reader
    text = ""  # Initialize empty string to hold text
    for page in pdf_reader.pages:  # Iterate over each page in the PDF
        text += page.extract_text() or ""  # Extract text from each page
    return text  # Return the extracted text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],  # Define separators for splitting
        chunk_size=10000,  # Define chunk size
        chunk_overlap=1000,  # Define chunk overlap
    )
    chunks = text_splitter.split_text(text)  # Split text into chunks
    return chunks  # Return the chunks

# Function to create vector store
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Initialize embeddings
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)  # Create vector store from text chunks
    vector_store.save_local("faiss_index")  # Save vector store locally
    return vector_store  # Return the vector store

# Function to format response
def format_response(response):
    sections = response.split("\n\n")  # Split response into sections
    formatted_response = ""  # Initialize empty string for formatted response
    for section in sections:  # Iterate over each section
        if section.strip():  # Check if section is not empty
            heading, content = section.split("\n", 1)  # Split section into heading and content
            formatted_response += f"### {heading.strip()}\n"  # Add formatted heading
            formatted_response += f"{content.strip()}\n\n"  # Add formatted content
    return formatted_response  # Return the formatted response

# Function to get base64 encoding of a file
def get_base64(file_path):
    with open(file_path, "rb") as f:  # Open file in binary read mode
        return base64.b64encode(f.read()).decode()  # Return base64 encoded string

# Function to add a logo to the Streamlit app
def add_logo(file_path, width='150px', height='50px', left='30px', top='20px'):
    bin_str = get_base64(file_path)  # Get base64 string of the logo file
    logo_html = f"""
    <header tabindex="-1" data-testid="stHeader" class="st-emotion-cache-h4xjwg ezrtsby2"><div data-testid="stDecoration" id="stDecoration" class="st-emotion-cache-1dp5vir ezrtsby1"></div>
    <img src="data:image/png;base64,{bin_str}" style="width: {width}; height: {height}; margin-left :{left}; margin-top:{top}"/>
    </header>
    """
    st.markdown(logo_html, unsafe_allow_html=True)  # Add the logo to the Streamlit app

# Define the Streamlit app
def main():
    st.set_page_config(layout="wide")  # Set page configuration for wide layout
    add_logo('./Caladin_Ai__1_-removebg-preview.png')  # Add logo to the app

    # Add heading and subheading to the app
    st.markdown("<h1 style='text-align: center;padding-bottom:20px;'>Get Detailed Risk of Bias <span style='color:rgb(5 110 207);'> Analysis </span></h1>", unsafe_allow_html=True)
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;margin-left:10%;margin-right:10%;margin-top:25px;'>Welcome to the Risk of Bias Analyser! Using the power of <span style='color:rgb(5 110 207);'> AI </span>, we provide a detailed risk of bias analysis for each domain of your research paper. Simply upload your PDF and click 'Analyse' to get started.</h4>", unsafe_allow_html=True)
    
    # File uploader for PDF files
    uploaded_file = st.file_uploader("")

    # CSS for styling the file uploader and other elements
    css = '''
    <style>
        [data-testid='stFileUploader'] section {
            padding: 0;
            margin-left: 21%;
            margin-right: 21%;
            margin-bottom: 20px;
            padding-top: 25px;
            padding-bottom: 25px;
            padding-left: 25px;
            padding-right: 25px;
            border-radius: 10px;
        }
        [data-testid='stFileUploader'] section > input + div {
            display: center;
        }
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)

    st.markdown("""
    <style>
        .main-content {
            padding: 0.7px;
            margin-left: 30%;
            margin-right: 30%;
            background-color: #f9f9f9;
            border-radius: 10px;
        }
        .stHeader {
            text-align: center;
        }
        .logostyle {
            display: flex;
        }
        .css-5uatcg {
            background-color: rgb(5, 110, 207);
            padding: 10px;
        } 
        .css-5uatcg:hover {
            color: #000;
            border-color: #000;
        }
        .css-5uatcg:active {
            color: #000;
            border: 1px solid green;
            background-color: green;
        }
        .st-emotion-cache-fqsvsg {
            margin-left: 20%;
            margin-right: 21%;
        }
        .st-emotion-cache-1p1m4ay {
            display: none;
        }
        .css-5uatcg {
            margin-left: 21%;
        }
        #stMarkdownContainer {
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
            text-align: justify;
        }
        .st-emotion-cache-15hul6a {
            margin-left: 21%;
        }
        .css-1avcm0n {
            background: none;
        }
    </style>
    """, unsafe_allow_html=True)

    # Process the uploaded file
    if uploaded_file is not None:
        try:
            pdf_text = get_pdf_text(uploaded_file)  # Extract text from PDF
            text_chunks = get_text_chunks(pdf_text)  # Split text into chunks
            vector_store = get_vector_store(text_chunks)  # Create vector store
            prompt_text = construct_prompt(pdf_text)  # Construct prompt text
            
            st.markdown("""
            <style>
            div.stButton {
                margin-left: 21%;
            }
            div.stSpinner > div {
                height: 100px;
                margin-top: 10px;
                margin-left: 50%;
            }
            </style>""", unsafe_allow_html=True)
                    
            button = st.button("Analyse")  # Analyse button
            spinner = st.spinner('Analysing...')  # Spinner for analysis

            if button:
                with spinner:
                    generation_config = {
                        "candidate_count": 1,  # Number of candidates
                        "max_output_tokens": 10000,  # Maximum output tokens
                        "temperature": 1.0,  # Temperature for randomness
                        "top_p": 0.7,  # Top p for nucleus sampling
                    }

                    safety_settings = [
                        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]

                    model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config, safety_settings=safety_settings)
                    response = model.generate_content(prompt_text)  # Generate content using the model

                st.markdown("## Summary of Research Paper")  # Display summary header
                st.markdown(response.text)  # Display the generated response
                print(response)  # Print the response for debugging

        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {e}")  # Display error message if any

    st.markdown("</div>", unsafe_allow_html=True)  # End of the main content div

if __name__ == "__main__":
    main()  # Run the main function
