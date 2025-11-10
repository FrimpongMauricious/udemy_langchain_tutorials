import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from langchain_community.document_loaders import WebBaseLoader



os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_TRACING_PROJECT_NAME'] = 'landgraph-practice'

import os
import streamlit as st


# def loadWebsite(url):
#     loader = WebBaseLoader(url)
#     data = loader.load()
#     return data


user_url = st.text_input("please enter a valid website address here")
prompt = PromptTemplate(
    input_variables = ['question','context'],
    template = """ You are an expert website scraper. Given the following website content: {context}, you are to answer the question: {question}
    
    use only the information from the website and nothing else. if the user question is not found in the infor returned in the website data provided, tell the user that "you are not
    able to find the information on the website provided".
    
    do not make up any answers. Provide your answer in a concise manner.
    
    """
)

user_question = st.text_input("please what is your question regarding the website content (summarise, explain, specific details, etc)")


# user_url = st.text_input("please enter a valid website address here")


# def loadWebsite(url):
#     loader = WebBaseLoader(url)
#     data = loader.load()
#     return data

output_parser = StrOutputParser()
llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0)
chain = prompt | llm | output_parser


answer_button = st.button("Get Answer")

if answer_button:
    if not user_url:
        st.warning("Please enter a valid website URL.")
    elif not user_question:
        st.warning("Please enter your question regarding the website content.")
    else:
        with st.spinner("Getting you an answer..."):
            loader = WebBaseLoader(user_url)
            data  = loader.load()
            
            extracted_data = data[0].page_content
            
            
            reply = chain.invoke({
            'question': user_question,
            'context':  extracted_data
                })
            st.write(reply)
        
        


