import os
import time
from PyPDF2 import PdfReader
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from prompt import construct_prompt
import base64

# Load environment variables
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# Function to extract text from PDF
def get_pdf_text(pdf_path):
    pdf_reader = PdfReader(pdf_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=10000, 
        chunk_overlap=1000,
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create vector store
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return vector_store

def format_response(response):
    sections = response.split("\n\n")
    formatted_response = ""
    for section in sections:
        if section.strip():
            heading, content = section.split("\n", 1)
            formatted_response += f"### {heading.strip()}\n"
            formatted_response += f"{content.strip()}\n\n"
    return formatted_response

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# def set_background_image(file_path):
#     bin_str = get_base64(file_path)
#     page_bg_img = f"""
#     <style>
#         [data-testid="stHeader"] {{
#              url("data:image/png;base64,{bin_str}");
#             width: ;
#         }}
#     </style>
#     """
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# Example usage to set the header background
def add_logo(file_path, width='150px', height='50px'):
    bin_str = get_base64(file_path)
    logo_html = f"""
    <header tabindex="-1" data-testid="stHeader" class="st-emotion-cache-h4xjwg ezrtsby2"><div data-testid="stDecoration" id="stDecoration" class="st-emotion-cache-1dp5vir ezrtsby1"></div>
    <img src="data:image/png;base64,{bin_str}" style="width: {width}; height: {height};"/>
    </header>
    """
    st.markdown(logo_html, unsafe_allow_html=True)
# Define the Streamlit app
def main():
    st.set_page_config(layout="wide")
    add_logo('./Caladin_Ai__1_-removebg-preview.png')
    # header = f"""
    # <header tabindex="-1" data-testid="stHeader" class="st-emotion-cache-h4xjwg ezrtsby2"><div data-testid="stDecoration" id="stDecoration" class="st-emotion-cache-1dp5vir ezrtsby1"></div>
    # <img src="https://media.istockphoto.com/id/920877788/photo/self-drive-autonomous-vehicle.jpg?s=612x612&w=0&k=20&c=ZouPkmrckgky1V8zZ6l6_lHzD1ilkE0dQwEGo70r17Y=" alt="Girl in a jacket" width="150" height="50">
    # </header>
    # """
    # st.markdown(header,unsafe_allow_html=True)
    # st.markdown("<h1 style='text-align: center;padding-top:-100px;'>Risk of Bias Analyser</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;padding-bottom:20px;'>Get Detailed Risk of Bias <span style='color:rgb(5 110 207);'> Analysis </span></h1>", unsafe_allow_html=True)
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    
    st.markdown("<h4 style='text-align: center;margin-left:10%;margin-right:10%;margin-top:25px;'>Welcome to the Risk of Bias Analyzer! Using the power of <span style='color:rgb(5 110 207);'> AI </span>, we provide a detailed risk of bias analysis for each domain of your research paper. Simply upload your PDF and click 'Analyse' to get started.</h4>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("")

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
        
        .st-emotion-cache-1p1m4ay{
            display:None;
        }
        .css-5uatcg {
            margin-left: 21%;
        }
        #stMarkdownContainer {
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
            text-align: justify;
        }
        .st-emotion-cache-15hul6a{
            margin-left:21%;
        }
        
        .css-1avcm0n{
            <img src="/Caladin Ai (1).png" alt="logo"/>
        }
        .css-1avcm0n {
            background: none;
        }
    </style>
    """, unsafe_allow_html=True)
    

    if uploaded_file is not None:
        try:
            pdf_text = get_pdf_text(uploaded_file)
            text_chunks = get_text_chunks(pdf_text)
            vector_store = get_vector_store(text_chunks)
            prompt_text = construct_prompt(pdf_text)
            st.markdown("""
            <style>
            div.stSpinner > div {
                # text-align:left;
                # align-items: left;
                # justify-content: left;
                height:100px;
                margin-top:10px;
                margin-left:50%;
            }
            </div>
            </style>""", unsafe_allow_html=True)
                    
            button = st.button("Analyse",)
            spinner = st.spinner('Analysing...')

            if button:
                with spinner:
                    generation_config = {
                        "candidate_count": 1,
                        "max_output_tokens": 10000,
                        "temperature": 1.0,
                        "top_p": 0.7,
                    }

                    safety_settings = [
                        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]

                    model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config, safety_settings=safety_settings)
                    response = model.generate_content(prompt_text)

                st.markdown("## Summary of Research Paper")
                st.markdown(response.text)
                print(response)

        except Exception as e:
            st.error(f"An error occurred while processing the PDF: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
