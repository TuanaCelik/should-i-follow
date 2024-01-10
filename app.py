
from annotated_text import annotation
from json import JSONDecodeError
import logging
from markdown import markdown
import requests

import streamlit as st

from utils.haystack import query, start_haystack
from utils.ui import reset_results, set_initial_state, sidebar

set_initial_state()

sidebar()

st.write("# 🐤 What have they been posting about lately on Mastodon?")

if st.session_state.get("OPENAI_API_KEY"):
    pipeline = start_haystack(st.session_state.get("OPENAI_API_KEY"))
    st.session_state["api_key_configured"] = True
    search_bar, button = st.columns(2)
    # Search bar
    with search_bar: 
        username = st.text_input("Please provide a Mastodon username", on_change=reset_results)

    with button: 
        st.write("")
        st.write("")
        run_pressed = st.button("Search posts (toots)")
else:
    st.write("Please provide your OpenAI Key to start using the application")
    st.write("If you are using a smaller screen, open the sidebar from the top left to provide your OpenAI Key 🙌")
    
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
                st.session_state.result = query(username, pipeline)
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
            