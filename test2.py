import os
import time

import openai
import streamlit as st
# Create an OpenAI client with your API key
openai_client = openai.Client(api_key='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')

# Retrieve the assistant you want to use
assistant = openai_client.beta.assistants.retrieve(
    "asst_4aKW0s2a8ygnEQo5NLNC0tG3"
)
# Create the title and subheader for the Streamlit page
st.title("Deep Learning and pattern recognition Tutor")
st.subheader("ask questions about the course")
thread_id = openai_client.beta.threads.create()
thread = thread_id.id
placeholder ="Can you give me a short summary?"

question = st.text_input(
    "put your question here",
    placeholder ="Can you give me a short summary?",
   
    )
send_button = st.button("Send")

# Check if send button is clicked
if send_button and question:
    with st.status("Starting work...", expanded=True) as status_box:
       
        #     # Create a status indicator to show the user the assistant is working
        #     with st.status("Starting work...", expanded=False) as status_box:
        #         # Upload the file to OpenAI

            # Create a new thread with a message that has the uploaded file's ID
        openai_client.beta.threads.messages.create(
        thread,
        role = "user",
        content = question
        )

        # Create a run with the new thread
        run = openai_client.beta.threads.runs.create(
            thread_id=thread,
            assistant_id=assistant.id,
            )

        # Check periodically whether the run is done, and update the status
        while run.status != "completed":
            time.sleep(5)
            status_box.update(label=f"{run.status}...", state="running")    
            run = openai_client.beta.threads.runs.retrieve(
                thread_id=thread, run_id=run.id
            )

        # Once the run is complete, update the status box and show the content
        status_box.update(label="Complete", state="complete", expanded=True)
        messages = openai_client.beta.threads.messages.list(
            thread_id=thread
        )
        st.markdown(messages.data[0].content[0].text.value)