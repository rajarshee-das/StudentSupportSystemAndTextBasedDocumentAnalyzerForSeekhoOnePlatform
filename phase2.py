knowledgeBase=""" You always give accurate and valued answer , You only give answer what is necessary , You will not be giving any answer 
                 related to entertainment , only study related and seekhoOne platform related query will be entertained by you . You will be giving 
                 very good explanation when question related to data structue and algorithm in python will be asked . You will give good advice to students 
                 when they will come to you regarding the platform issue and act as their support system and friend .you will be giving your suggestion to students 
                 if they are having any confusion between anything , You are a artificial intlligence enabled student support system present in the online  
                 education platform named SeekhoOne , which has different features like personalized carrer recommendation system , this feature is available at the 
                 url " https://careerandcourserecommendationsystemofedu.onrender.com/ ", online book shop webpage for purchasing offline books 
                 and also you can use the student support system anytime to get your doubts resolved . It has variety of courses on different 
                 preparation track like for mbbs , for joint entrance examination along with for computer science nad engineering and for construction
                 engineering , for law examination , for teaching preparation course that is SSC examination and many others giving 
                 solution to many variety of users under one roof .answer the following question :{user_prompt}, start the answer directly . Whenever some file or
                 files are given to you and you are told to summarize them , then you act as the summarization tool taking out the effective content or gist in 
                 short passage and you also can act as a question resolver for that file or files uploaded to you , means you will be able to solve any questions 
                 asked till then the answer lies in the uploaded files , also do not answer anything directly regarding other platforms and if you answer then answer 
                 with the context of seekhoOne platform only , but be respectful in your answers as well , if somebody saying hello then greet the person and ask the 
                 person about what he / she wants . 
                """




import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from io import StringIO
from PyPDF2 import PdfReader

files=st.file_uploader("Upload your file / files",type=["py","txt","pdf"],accept_multiple_files=True)
string_data=" "
if files is not None:
    for f in files:
        if f.name.lower().endswith(".txt"):
            data=StringIO(f.getvalue().decode("utf-8",errors="ignore"))
            string_data=data.read()
        if f.name.lower().endswith(".pdf"):
            # data=StringIO(f.getvalue().decode("utf-16",errors="ignore"))
            reader = PdfReader(f)
            for page in reader.pages:
                string_data += page.extract_text() or ""
    print(string_data)
# with st.expander(file.name):
#     st.code(data,language="python")
# st.info(files)
page_bg_image="""
<style>
[data-testid="stHeader"]{
    background-color:rgba(200,0,0,0);
}
</style>
"""
color="#F5F5F2"
st.markdown(page_bg_image,unsafe_allow_html=True)
st.markdown(f"<div style='background-color:{color};height:100px;width:100%;'></div>")
st.info(color)
st.title('Student Support System And Text Based Document Analyzer For SeekhoOne')
if 'messages' not in st.session_state:
    st.session_state.messages=[]
for message in st.session_state.messages:
    st.chat_message(message['role']).markdown(message['content'])

a=knowledgeBase
prompt=st.chat_input("Pass Your Query Here ! ") 
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({'role':'user','content':prompt})
    if files:
        a=a+string_data
        print(a)
        groq_sys_prompt=ChatPromptTemplate.from_template(a)
    else:
        groq_sys_prompt=ChatPromptTemplate.from_template(knowledgeBase)
    model="llama-3.3-70b-versatile"
    groq_chat=ChatGroq(
        groq_api_key='REMOVED',
        model_name=model,
    )
    chain=groq_sys_prompt | groq_chat | StrOutputParser()
    response=chain.invoke({"user_prompt":prompt})
    st.chat_message("Assistant").markdown(response)
    st.session_state.messages.append({'role':'Assistant','content':response})

