import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from whisperiss import listening,speak
import warnings
from yolois import eyes
from dotenv import load_dotenv
from clip import generate_captions
import os

load_dotenv()

warnings.filterwarnings("ignore",category=UserWarning,module='whisper.transcribe',lineno=114)
warnings.filterwarnings("ignore",message = "FP16 is not supported on CPU; using FP32 instead")

serper_api_key = os.getenv("SERPER_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
template = """You are an AI assistant. Use the previous conversation for context:
{chat_history}
User: {user_input}
AI:"""
prompt = PromptTemplate(input_variables=["chat_history", "user_input"], template=template)
llm = ChatGroq(groq_api_key=groq_api_key , model_name="llama-3.2-11b-vision-preview")
chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

listis="Listening"
while True:
    lis="Do you wanna me to see , listen or exit ? "
    print(lis)
    speak(lis) 
    propis = listening()
    print(propis)
    if "listen" in propis.lower().strip():
        print("Listening...")
        speak(listis)
        prop = listening() 
        if "use google" in prop.lower().strip():
            toolsis = load_tools(["google-serper"])
            agent = initialize_agent(toolsis, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)
            print("Transcribed Audio:", prop)
            response = agent.run(prop)
            print("\033[34m"+"Generated Response: "+ response+"\033[0m")
            speak(response)
            
        else:
            summ = PromptTemplate(input_variables=[], template=prop)
            print(prop)
            # chain = LLMChain(llm=llm, prompt=summ)
            response = chain.run(user_input=prop)
            print("\033[34m"+"Generated Response: "+ response+"\033[0m")
            speak(response)
            
    elif "exit" in propis.lower().strip():
        break
    else:
        speak("Seeing")
        eyes()
        txt1=generate_captions(r'captured_image.jpg')
        print("Listening...")
        speak(listis)
        prop = listening() 
        promptis= f" Given one description of the scene as {txt1}  . Treat all the answers for the same scene but with different details. Use all the details and answer the question using the above information as detailed and as accurately according to the information provided as possible. Do not make any assumptions from your side. {prop}"
        print("Transcribed Audio:", prop)
        if "use google" in promptis.lower().strip():
            toolsis = load_tools(["google-serper"])
            agent = initialize_agent(toolsis, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
            response = agent.run(promptis)
            print("\033[34m"+"Generated Response: "+ response+"\033[0m")
            speak(response)
        else:  
            summ = PromptTemplate(input_variables=[], template=promptis)
            imagechain = LLMChain(llm=llm, prompt=summ)
            response = imagechain.run(user_input=prop)
            print("\033[34m"+"Generated Response: "+ response+"\033[0m")
            speak(response)

