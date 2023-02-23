
from annotated_text import annotation
from json import JSONDecodeError
import logging
from markdown import markdown

import streamlit as st

from utils.haystack import query
from utils.ui import reset_results, set_initial_state

set_initial_state()

st.markdown("Thanks for coming to this 🤗 Spcae.\n **A few words of warning**:\n\n"
        "This is very much a project for fun, and is not a final product."
        "There's a lot that can be improved to make this app better...\n\n"
        "**Please take results with a grain of** 🧂\n\n"
        "For more on how this was built, instructions to run locally and to contribute: [visit GitHub](https://github.com/TuanaCelik/should-i-follow#readme)")

st.write("# 🐤 What have they been tweeting about lately?")

search_bar, button = st.columns(2)
# Search bar
with search_bar: 
    username = st.text_input("Please provide a twitter username", on_change=reset_results)

with button: 
    st.write("")
    st.write("")
    run_pressed = st.button("Search tweets")

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
        