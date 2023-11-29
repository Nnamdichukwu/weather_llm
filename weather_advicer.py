import os

from langchain.document_loaders import WeatherDataLoader
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage
import streamlit as st

openai_api_key = st.secrets["openai_api_key"]
weather_open_api_key = st.secrets["weather_open_api_key"]
st.set_page_config(page_title="Weather Helper", page_icon=":robot:")
st.header("Weather Helper")


template = (
    """
    %INSTRUCTIONS:
    You are a helpful AI that gets their {location} and then tells them the current weather as well as what they should wear for that weather. 
    Output the weather response in this format- Today's weather in {location}: The temperature is {temperature}°C.
    
    After this, advice them on what to wear. 
    
    If the weather is too hot tell them to get a sunscreen, and advice they should wear something light. 
    
    If they weather is too cold advice they should be properly covered and layered to insulate them from the cold.
    
    Provide as much useful information on the their clothing and the weather in general. You are to be very helpful
    %TEXT:
    {text}
    """
    
)

def load_llm():
   try:
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    llm =  ChatOpenAI(temperature=1, model_name = 'gpt-3.5-turbo',openai_api_key=openai_api_key)

    loader = WeatherDataLoader.from_params(
                {location}, openweathermap_api_key=weather_open_api_key)
    
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template) 
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    documents = loader.load()
    generated_response= llm(
        chat_prompt.format_prompt(
            location=location,condition=documents, temperature=documents, text=location
        ).to_messages()
    )
    return generated_response.content
   except Exception as e:
            print(e)
   


st.markdown("This is a helpful AI that tells you the weather in a particular location and provides advice on what to wear. All you have to provide is the location you want to get the weather of")



st.markdown("## Enter the location")
location =st.text_input(label="What location are you interested in... ",  placeholder="Ex: Lagos...", key="location")
weather_llm =load_llm()

st.write(weather_llm)
