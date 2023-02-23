
from annotated_text import annotation
from json import JSONDecodeError
import logging
from markdown import markdown
import requests

import streamlit as st

from utils.haystack import start_haystack, query
from utils.ui import reset_results, set_initial_state, sidebar
from utils.config import TWITTER_BEARER

set_initial_state()

st.write("# 🐤 What have they been tweeting about lately?")

sidebar()


if st.session_state.get("OPENAI_API_KEY"):
    prompter, template = start_haystack(st.session_state.get("OPENAI_API_KEY"))
    st.session_state["api_key_configured"] = True
    search_bar, button = st.columns(2)
    # Search bar
    with search_bar: 
        username = st.text_input("Please provide a twitter username", on_change=reset_results)

    with button: 
        st.write("")
        st.write("")
        run_pressed = st.button("Search tweets")
else:
    st.write("Please provide your OpenAI Key to start using the application")
    
if st.session_state.get("api_key_configured"):
    run_query = (
        run_pressed or username != st.session_state.username
    )

    # Get results for query
    if run_query and username:
        reset_results()
        st.session_state.username = username
        with st.spinner("🔎"):
            try:
                st.session_state.result = query(username, prompter, template)
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
            