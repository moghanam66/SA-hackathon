import streamlit as st
import pandas as pd
import re
from deep_translator import GoogleTranslator
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain,SequentialChain
from langchain.prompts import ChatPromptTemplate
import base64

@st.cache_data
def openAiPlaner(question,placesDf,API_KEY):
    llm = ChatOpenAI(openai_api_key=API_KEY,temperature=0)

    # prompt template 1: translate to english
    first_prompt = ChatPromptTemplate.from_template(
        "This is a question from a tourist visiting Saudi Arabia:"
        "\n\n{Question}"
        f"\n\n Suggest 10 places to visit from this list{placesDf}")

    # chain 1: input= Review and output= English_Review
    chain_one = LLMChain(llm=llm, prompt=first_prompt,
                        output_key="places")
    # prompt template 1: translate to english
    second_prompt = ChatPromptTemplate.from_template(
        "Create a plan to visit those places:"
        "\n\n{places}")

    chain_two = LLMChain(llm=llm, prompt=second_prompt,
                        output_key="plane")
    overall_chain = SequentialChain(chains=[chain_one,chain_two],
    input_variables=["Question"],
    output_variables=["places",'plane'],
    verbose=True)
    return overall_chain(question)

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
    

st.set_page_config(
    page_title='Plan your vacation',
    page_icon=":star:",layout="wide")

# set_background('_2f6e1e1c-5229-4fce-8241-9beea9c29c5d.jpeg')

OPENAI_API_KEY = st.secrets["openAI_API"]
st.title('Tell us what you want to do and let AI plan your stay for you.')

dfEng=pd.read_csv('attractionsEng.csv')
placesDf=list(dfEng['attractionSite'])


user_input = st.text_input(" What do you want to do in Saudi ?",'I want to visit fun sites')
if user_input !='':
    
    answer=openAiPlaner(user_input,placesDf,OPENAI_API_KEY)
    plane=answer['plane']
    places=answer['places'].split('\n')
    days=plane.split('\n\n')
    for day in days:
        if re.fullmatch('^[\u0621-\u064A0-9 ]+$',user_input):
            dayAr=GoogleTranslator(source='en',target='ar').translate(day).replace('-','\n-')
            st.markdown("<div style='direction: RTL;'> {} </div>".format(dayAr), unsafe_allow_html=True)
        else:
            st.markdown(day)
        placesToDisplay=[place[3:].strip() for place in places if place[3:].strip() in day]
        nuOfImages=plane.count('-')
        images=[]
        captions=[]
        for placeToDisplay in placesToDisplay:
            image=dfEng[dfEng['attractionSite']==placeToDisplay]['image'].values
            if len(image)>0:
                if re.fullmatch('^[\u0621-\u064A0-9 ]+$',user_input):
                    placeToDisplay=GoogleTranslator(source='en',target='ar').translate(placeToDisplay)
                images.append(image[0])
                captions.append(placeToDisplay)
        st.image(images,caption=captions,width=300)


    
