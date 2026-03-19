import streamlit as st
from pathlib import Path
from utils.bluesky import BlueskyFetcher
from haystack import Pipeline
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.builders import ChatPromptBuilder
from haystack.utils.auth import Secret

def start_haystack(openai_key):
    fetcher = BlueskyFetcher()

    prompt_template = Path("prompt_template.txt").read_text()
    prompt_builder = ChatPromptBuilder(template=prompt_template, required_variables="*")
    llm = OpenAIChatGenerator(model="gpt-4.1-nano", api_key=Secret.from_token(openai_key))

    pipeline = Pipeline()
    pipeline.add_component("fetcher", fetcher)
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("llm", llm)


    pipeline.connect("fetcher.documents", "prompt_builder.documents")
    pipeline.connect("prompt_builder.prompt", "llm.messages")

    st.session_state["haystack_started"] = True

    return pipeline


@st.cache_data(show_spinner=True)
def query(username, _pipeline):
    try:
        replies = _pipeline.run(data={"fetcher": {"username": username,
                                                 "last_k_posts": 20}})
        result = replies['llm']['replies'][0].text
    except Exception as e:
        result = ["Please make sure you are providing a correct, public Bluesky account"]
    return result