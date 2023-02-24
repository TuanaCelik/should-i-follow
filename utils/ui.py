import streamlit as st
from PIL import Image

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
        image = Image.open('logo/haystack-logo-colored.png')
        st.markdown("Thanks for coming to this 🤗 Space.\n\n"
        "This is a project for fun, and is not a final product."
        " There's a lot that can be improved to make this app better.\n\n"
        "**Take results with a grain of** 🧂\n\n"
        "For more on how this was built, instructions to run locally and to contribute: [visit GitHub](https://github.com/TuanaCelik/should-i-follow#readme)")

        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below\n"
            "2. Enter a Twitter username in the searchbar\n"
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
        st.markdown(
            "## How this works\n"
            "This app was built with [Haystack](https://haystack.deepset.ai) using the"
            " [`PromptNode`](https://docs.haystack.deepset.ai/docs/prompt_node) and custom [`PromptTemplate`](https://docs.haystack.deepset.ai/docs/prompt_node#templates).\n\n"
            " The source code is also on [GitHub](https://github.com/TuanaCelik/should-i-follow)"
            " with instructions to run locally.\n"
            "You can see how the `PromptNode` was set up [here](https://github.com/TuanaCelik/should-i-follow/blob/main/utils/haystack.py)")
        st.markdown("---")
        st.markdown("Made by [tuanacelik](https://twitter.com/tuanacelik)")
        st.markdown("---")
        st.markdown("""Thanks to [mmz_001](https://twitter.com/mm_sasmitha) 
                        for open sourcing [KnowledgeGPT](https://knowledgegpt.streamlit.app/) which helped me with this sidebar 🙏🏽""")
        st.image(image, width=250)