import streamlit as st
from agent import Agent
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
import re

prompt = """
Eres un agente de inteligencia artificial creado para ayudar a la empresa AutoCare en su proceso de transformación digital. Tu función principal es optimizar la experiencia del cliente, proporcionando respuestas claras y precisas sobre modelos de vehículos, opciones de financiamiento, y servicios de mantenimiento, a la vez que programas citas para pruebas de manejo y mantenimiento. Además, asistirás a los clientes en la resolución de problemas técnicos básicos, guiándolos a través de procesos de diagnóstico simples. Recogerás feedback valioso para mejorar continuamente los servicios de AutoCare y generarás informes que faciliten la toma de decisiones estratégicas. Trabajarás 24/7, asegurando que todos los clientes reciban atención inmediata. Utiliza datos en tiempo real para ofrecer una experiencia personalizada, pero siempre garantizando la seguridad y la privacidad de la información. Recuerda que tu rol también incluye facilitar la adopción de nuevas tecnologías entre los empleados de AutoCare, promoviendo una cultura colaborativa
"""

tools = None

if tools:
    agent = Agent(model_type="groq", prompt=prompt, tools=tools)
else:
    agent = Agent(model_type="groq", prompt=prompt)


st.title("Agent Chat Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display all previous chat messages
for message in st.session_state.messages:
    if isinstance(message, (HumanMessage, AIMessage)) and message.content:
        with st.chat_message("user" if isinstance(message, HumanMessage) else "assistant"):
            st.markdown(message.content)


# React to user input
if prompt := st.chat_input("User input"):
    # Create a HumanMessage and add it to chat history
    human_message = HumanMessage(content=prompt)
    st.session_state.messages.append(human_message)

    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)

    # Invoke the agent to get a list of AI messages, including potentially retrieved documents
    response_messages = agent.invoke(st.session_state.messages)

    # Update the session state with the new response
    st.session_state.messages = response_messages["messages"]

    # Display only the last AI message with content
    last_message = response_messages["messages"][-1]


    if isinstance(last_message, AIMessage) and last_message.content:
        st.chat_message("assistant").markdown(last_message.content)

    
