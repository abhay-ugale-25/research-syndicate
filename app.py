import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000/research")

# PAGE SETUP

st.set_page_config(page_title="Research Syndicate", page_icon=":writing_hand:", layout="centered")

st.title("Research Syndicate")
st.markdown("Enter a complex technical topic, and our LangGraph agents will autonomously search the deep web, evaluate sources, and synthesize a fully cited report.")

# USER INPUT

topic = st.text_input("Research Topic", placeholder="Enter a complex technical topic")

if st.button("Generate Report", type="primary"):
    if not topic:
        st.warning("Please enter a topic")
    else:
        with st.spinner("Generating report... This may take a while."):
            try:
                response = requests.post(API_URL, json={"topic": topic}, timeout = 200)
                if response.status_code == 200:
                    response_data = response.json()
                    st.success("Success!")
                    st.divider()
                    st.markdown(response_data["report"])
                else:
                    st.error(f"Error: {response.status_code}")
                    st.error(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
            
    