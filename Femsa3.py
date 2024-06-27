import streamlit as st
from openai import OpenAI
import time

# Create client

st.title(':book: : Análisis de casos')

# Initialize chat history (using session_state)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize state for enabling the "Agregar otro caso" button
if "enable_add_button" not in st.session_state:
    st.session_state.enable_add_button = False

# Display chat history
for message in st.session_state.messages:
    with st.container():
        st.markdown(f"**{message['role']}:** {message['content']}")

# Input text box for API key
user_input_key = st.text_input("API KEY OPEN IA:", "")

client = OpenAI(api_key=user_input_key)

# Input text area for case
user_input = st.text_area("Caso:", "", height=500)

if st.button("Analizar") and user_input:
    # Add user message to chat history
    #st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message immediately
    #with st.container():
       # st.markdown(f"**You:** {user_input}")

    # Create thread and message 
    thread = client.beta.threads.create()
    thread_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input,
    )
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id='asst_tD7CXWtjMZEVP6iChWE9vcek'  # Replace with your assistant ID
    )
    
    # Wait for the run to complete
    with st.spinner("Thinking..."):
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            time.sleep(0.5)

    # Retrieve and display the response
    messages = client.beta.threads.messages.list(thread_id=thread.id).data
    latest_message = messages[0]
    response_text = latest_message.content[0].text.value

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    # Display assistant message immediately
    with st.container():
        st.markdown(f"**Respuesta al análisis del caso:** {response_text}")

    # Enable the "Agregar otro caso" button
    st.session_state.enable_add_button = True

# Button to add another case and refresh the page
if st.session_state.enable_add_button:
    if st.button("Agregar otro caso"):
        st.session_state.messages = []
        st.session_state.enable_add_button = False
        # Reset the input text area
        st.experimental_rerun()
