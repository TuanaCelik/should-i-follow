import streamlit as st
from mastodon_fetcher_haystack.mastodon_fetcher import MastodonFetcher
from haystack import Pipeline
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import PromptBuilder

def start_haystack(openai_key):
    #Use this function to contruct a pipeline
    fetcher = MastodonFetcher()

    mastodon_template = """You will be given a post stream belonging to a specific Mastodon profile. Answer with a summary of what they've lately been posting about and in what languages.
                            You may go into some detail about what topics they tend to like postint about. Please also mention their overall tone, for example: positive,
                            negative, political, sarcastic or something else.

                            Examples: 
                            
                            Post stream: [@deepset_ai](https://mastodon.social/@deepset_ai): Come join our Haystack server for our first Discord event tomorrow, a deepset AMA session with @rusic_milos @malte_pietsch…
                            [@deepset_ai](https://mastodon.social/@deepset_ai): Join us for a chat! On Thursday 25th we are hosting a 'deepset - Ask Me Anything' session on our brand new Discord. Come…
                            [@deepset_ai](https://mastodon.social/@deepset_ai): Curious about how you can use @OpenAI GPT3 in a Haystack pipeline? This week we released Haystack 1.7 with which we introdu…
                            [@deepset_ai](https://mastodon.social/@deepset_ai): So many updates from @deepset_ai today! 
                            
                            Summary: This user has lately been reposting posts from @deepset_ai. The topics of the posts have been around the Haystack community, NLP and GPT. They've
                            been posting in English, and have had a positive, informative tone.
                            
                            Post stream: I've directed my team to set sharper rules on how we deal with unidentified objects.\n\nWe will inventory, improve ca… 
                            the incursion by China’s high-altitude balloon, we enhanced radar to pick up slower objects.\n \nBy doing so, w…
                            I gave an update on the United States’ response to recent aerial objects. 

                            Summary: This user has lately been posting about having sharper rules to deal with unidentified objects and an incursuin by China's high-altitude
                            baloon. Their pots have mostly been neutral but determined in tone. They mostly post in English.

                            Post stream: {{ documents }}
                                            
                            Summary: 
                            """
    prompt_builder = PromptBuilder(template=mastodon_template)
    llm = OpenAIGenerator(model_name="gpt-4", api_key=openai_key)

    st.session_state["haystack_started"] = True   

    mastodon_pipeline = Pipeline()
    mastodon_pipeline.add_component("fetcher", fetcher)
    mastodon_pipeline.add_component("prompt_builder", prompt_builder)
    mastodon_pipeline.add_component("llm", llm)


    mastodon_pipeline.connect("fetcher.documents", "prompt_builder.documents")
    mastodon_pipeline.connect("prompt_builder.prompt", "llm.prompt")

    return mastodon_pipeline


@st.cache_data(show_spinner=True)
def query(username, _pipeline):
    try:
        replies = _pipeline.run(data={"fetcher": {"username": username,
                                                 "last_k_posts": 20}})
        result = replies['llm']['replies']
    except Exception as e:
        result = ["Please make sure you are providing a correct, public Mastodon account"]
    return result