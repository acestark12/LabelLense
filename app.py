import streamlit as st
from dotenv import load_dotenv
import nltk
import tempfile
from nltk.corpus import stopwords 
import os
import easyocr
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
#from dotenv import load_dotenv

st.set_page_config(page_title="Chat with LabelLense", page_icon="🔍")

def get_answer_from_gpt(question,messages):
    messages.append(HumanMessage(content=question))
    answer=chat.invoke(messages).content
    messages.append(AIMessage(content=answer))
    return answer

def get_keywords(img):
    reader=easyocr.Reader(['en'])
    result=reader.readtext(img)
    output=""
    for i in result:
         output+=i[1]+" "

    keywords=[]
    tokens = nltk.word_tokenize(output)
    stop_words = set(stopwords.words('english'))
    filtered_text = [word for word in tokens if not word.lower() in stop_words]
    for word in filtered_text:
        if word.isalpha():
            keywords.append(word.lower())
        keywords=list(set(keywords))   
    print(keywords)###############--------------------######################------------##########     
    return keywords

def save_uploaded_file(uploaded_file):
    # Save the uploaded file to a temporary file and return its path
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_path = temp_file.name

    try:
        temp_file.write(uploaded_file.read())
    finally:
        temp_file.close()

    return temp_file_path

def main():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history=[
        SystemMessage(content="You're a helpful assistant that describes health realted terms in short, its healthy level in body and tips to keep it balanced in body."),
    ]
    if "previous_messages" not in st.session_state:
        st.session_state.previous_messages = []

    if "keywords" not in st.session_state:
        st.session_state.keywords=[]
    
    if "definition" not in st.session_state:
        st.session_state.definition=""
 
    st.header("Your product's key contents :heavy_exclamation_mark:")
    
    with st.sidebar:
        st.subheader("Your Label")
        file_uploaded = st.file_uploader("Upload your label here and click on 'Process'")
        print(file_uploaded)
        if st.button("Process"):
            temp_path=save_uploaded_file(file_uploaded)
            keywords=get_keywords(temp_path)
            kw_str=''
            for word in keywords:
                st.write(word)
                kw_str=kw_str+word+', '
            query=[SystemMessage(content="""You are a helpful assistant that identifies the terms directly or indirectly related to packaged food ingredients, preservatives,
                                 nutritional contents of a food, and similar type of words from the list of words provided,
                                 and defines them in short, mentions its nutritional level in terms of scientific units and health related infomation ."""),
                                 HumanMessage(content=kw_str)]
            st.session_state.definition=chat.invoke(query).content

            
    if st.session_state.definition:
        st.write(st.session_state.definition)
    
    st.header("Ask LabelLense🔍...")
    for message in st.session_state.previous_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt:=st.chat_input("I am your LabelLense. How may I help you?"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.previous_messages.append({"role":"user","content":prompt})
        st.session_state.chat_history.append(HumanMessage(content=prompt))
        ai_response=chat.invoke(st.session_state.chat_history).content
        st.session_state.chat_history.append(AIMessage(content=ai_response))

        response=f"Genie:{ai_response}"
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.previous_messages.append({"role":"assistant","content":response})

if __name__ == "__main__":

    load_dotenv()
    nltk.download('punkt')
    nltk.download('stopwords')
    os.environ['OPENAI_API_KEY']=os.getenv('OPENAI_API_KEY')
    chat=ChatOpenAI()  
    main() 