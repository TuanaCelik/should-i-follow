
from annotated_text import annotation
from json import JSONDecodeError
import logging
from markdown import markdown

import streamlit as st

from utils.haystack import query
from utils.ui import reset_results, set_initial_state

set_initial_state()

st.write("# What have they been tweeting about lately?")

# Search bar
username = st.text_input("", value=st.session_state.username, max_chars=100, on_change=reset_results)

run_pressed = st.button("Run")

run_query = (
    run_pressed or username != st.session_state.username
)

# Get results for query
if run_query and username:
    reset_results()
    st.session_state.username = username
    with st.spinner("🔎"):
        try:
            st.session_state.result = query(username)
        except JSONDecodeError as je:
            st.error(
                "👓 &nbsp;&nbsp; An error occurred reading the results. Is the document store working?"
            )    
        except Exception as e:
            logging.exception(e)
            st.error("🐞 &nbsp;&nbsp; An error occurred during the request.")
        
            

if st.session_state.result:
    voice = st.session_state.result
    st.write(voice[0])
        