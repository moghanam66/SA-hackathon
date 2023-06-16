import streamlit as st
import pandas as pd
from streamlit_chat import message
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
import base64


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
    
@st.cache_data
def conversational_chat(query):
        
        result = chain({"question": query, 
        "chat_history": st.session_state['history']})
        st.session_state['history'].append((query, result["answer"]))
        
        return result["answer"]

st.set_page_config(
    page_title='Saudi Tourism',
    page_icon=":star:",layout="wide")

# set_background('_2f6e1e1c-5229-4fce-8241-9beea9c29c5d.jpeg')

OPENAI_API_KEY = st.secrets["openAI_API"]


dfEng=pd.read_csv('attractionsEng.csv')
placesDf=list(dfEng['attractionSite'])

  

tmp_file_path='FAQ.csv'
loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={
            'delimiter': ','})
data = loader.load()
    
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore = FAISS.from_documents(data, embeddings)

chain = ConversationalRetrievalChain.from_llm(
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,temperature=0.0,model_name='gpt-3.5-turbo'),
retriever=vectorstore.as_retriever())


    
    
if 'history' not in st.session_state:
        st.session_state['history'] = []

if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hello ! Ask any thing about tourism in KSA " +  " 🤗"]

if 'past' not in st.session_state:
    st.session_state['past'] = ["Hey ! 👋"]
    
#container for the chat history
response_container = st.container()
#container for the user's text input
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        
        user_input = st.text_input("Question:", placeholder=" ", key='input')
        submit_button = st.form_submit_button(label='Send')
        
    if submit_button and user_input:
        output = conversational_chat(user_input)
        
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
            
            
            
if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
            message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs") 


 
      
