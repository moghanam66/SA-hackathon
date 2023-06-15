import streamlit as st
from bardapi import Bard
import pandas as pd
import re
from streamlit_chat import message
from deep_translator import GoogleTranslator
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS
from transformers import MarianMTModel, MarianTokenizer
import os 
from streamlit_custom_notification_box import custom_notification_box
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

os.environ['OPENAI_API_KEY'] = st.secrets["openAI_API"]
bardtoken=st.secrets["Bard_API"]

@st.cache_data
def bardAnswer(user_input,places,bardtoken=bardtoken):
    bard = Bard(token=bardtoken)
    answer=bard.get_answer(f"give me a plan to vist the top ten sites that are suitable for this question ({user_input}) in this list ({places}) and their image url from this website https://www.visitsaudi.com")['content']
    return answer

dfEng=pd.read_csv('attractionsEng.csv')
places=list(dfEng['attractionSite'])

col1,col2=st.columns([0.5,0.5])
with col1:
    user_input = st.text_input(" What do you want to do in Saudi ?",'I want to vist fun sites')
    if user_input !='':
        
        answer=bardAnswer(user_input,places)

        imagesStringsUnfiltered = [
        answer[index+9:answer[index+9:].find(',')+index+9].strip('in') for index in range(len(answer))
        if answer.startswith('Image of', index)  
        ]   
        delimeters=re.findall(r"\[.*\]",answer)

        imagesStrings={}
        for i in delimeters:
            if ' in ' in i :
                imagesStrings[i]=i[:i.find(' in ')].replace('[Image of ','')
            else:
                imagesStrings[i]=i[:i.find(',')].replace('[Image of ','')

        
        for deli in delimeters:
            answer=answer.replace(deli,'<****>')
        answers=answer.split('<****>')

        for key,imageName in imagesStrings.items():
            image=dfEng[dfEng['attractionSite'].str.contains(imageName)]['image'].values
            if len(image)>0:
                imagesStrings[key]=image[0]
            else:
                imagesStrings[key]=''
        for i,answer in enumerate(answers):
            if re.fullmatch('^[\u0621-\u064A0-9 ]+$',user_input):
                answer=GoogleTranslator(source='en',target='ar').translate(answer)
                st.markdown("<div style='direction: RTL;'> {} </div>".format(answer), unsafe_allow_html=True)
            else:
                st.markdown(answer)

            if (i<len(delimeters)-1) and (imagesStrings[delimeters[i]] !=''):
                st.image(imagesStrings[delimeters[i]],caption=delimeters[i],width=300)

  
with col2:

    tmp_file_path='FAQ.csv'
    loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={
                'delimiter': ','})
    data = loader.load()
        
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(data, embeddings)

    chain = ConversationalRetrievalChain.from_llm(
    llm = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo'),
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
      
