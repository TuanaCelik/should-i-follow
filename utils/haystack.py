import streamlit as st
from mastodon_fetcher_haystack.mastodon_fetcher import MastodonFetcher
from haystack import Pipeline
from haystack.nodes import PromptNode, PromptTemplate

def start_haystack(openai_key):
    #Use this function to contruct a pipeline
    fetcher = MastodonFetcher()

    mastodon_template = PromptTemplate(prompt="""You will be given a post stream belonging to a specific Mastodon profile. Answer with a summary of what they've lately been posting about and in what languages.
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

                                                Post stream: {join(documents)}
                                                                
                                                Summary: 
                                                """)
    prompt_node = PromptNode(model_name_or_path="gpt-4", default_prompt_template=mastodon_template, api_key=openai_key)

    st.session_state["haystack_started"] = True   

    mastodon_pipeline = Pipeline()
    mastodon_pipeline.add_node(component=fetcher, name="MastodonFetcher", inputs=["Query"])
    mastodon_pipeline.add_node(component=prompt_node, name="PromptNode", inputs=["MastodonFetcher"])                                               
    return mastodon_pipeline


@st.cache_data(show_spinner=True)
def query(username, _pipeline):
    try:
        result = _pipeline.run(query=username, params={"MastodonFetcher": {"last_k_posts": 20}})
    except Exception as e:
        result = ["Please make sure you are providing a correct, public Mastodon account"]
    return result