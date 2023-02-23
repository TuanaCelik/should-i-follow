import streamlit as st

def set_state_if_absent(key, value):
    if key not in st.session_state:
        st.session_state[key] = value

def set_initial_state():
    set_state_if_absent("username", "Provide a Twitter username")
    set_state_if_absent("result", None)
    set_state_if_absent("haystack_started", False)

def reset_results(*args):
    st.session_state.result = None

def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key

def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"
            "2. Enter a twitter username in the searchbar\n"
            "3. Enjoy 🤗\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",
            value=st.session_state.get("OPENAI_API_KEY", ""),
        )

        if api_key_input:
            set_openai_api_key(api_key_input)

        st.markdown("---")
        st.markdown("### About\n"
                    "This app is just for fun and there are many points of improvement."
                    "It was built with [Haystack](https://haystack.deepset.ai) using the"
                    " [PromptNode](https://docs.haystack.deepset.ai/docs/prompt_node) and custom [PromptTemplate](https://docs.haystack.deepset.ai/docs/prompt_node#templates)"
                    "The source code is also on [GitHub](https://github.com/TuanaCelik/should-i-follow)"
                    "with instructions to run locally.")
        st.markdown("Made by [tuanacelik](https://twitter.com/tuanacelik)")
        st.markdown("---")
        st.markdown("""Thanks to [mmz_001](https://twitter.com/mm_sasmitha) 
                        for open sourcing [KnowledgeGPT](https://knowledgegpt.streamlit.app/) which helped me with this sidebar 🙏🏽""")