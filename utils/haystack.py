import streamlit as st
import requests
from utils.config import TWITTER_BEARER

from haystack.nodes import PromptNode, PromptTemplate

# cached to make index and models load only at start
@st.cache(hash_funcs={"builtins.CoreBPE": lambda _: None}, show_spinner=False, allow_output_mutation=True)
def start_haystack(openai_key):
    #Use this function to contruct a pipeline
    prompt_node = PromptNode(model_name_or_path="text-davinci-003", api_key=openai_key)


    twitter_template = PromptTemplate(name="twitter-voice", prompt_text="""You will be given a twitter stream belonging to a specific profile. Answer with a summary of what they've lately been tweeting about and in what languages.
                                                                    You may go into some detail about what topics they tend to like tweeting about. Please also mention their overall tone, for example: positive,
                                                                    negative, political, sarcastic or something else.

                                                                    Examples: 
                                                                    
                                                                    Twitter stream: RT @deepset_ai: Come join our Haystack server for our first Discord event tomorrow, a deepset AMA session with @rusic_milos @malte_pietsch…
                                                                    RT @deepset_ai: Join us for a chat! On Thursday 25th we are hosting a 'deepset - Ask Me Anything' session on our brand new Discord. Come…
                                                                    RT @deepset_ai: Curious about how you can use @OpenAI GPT3 in a Haystack pipeline? This week we released Haystack 1.7 with which we introdu…
                                                                    RT @tuanacelik: So many updates from @deepset_ai today! 
                                                                    
                                                                    Summary: This user has lately been retweeting tweets fomr @deepset_ai. The topics of the tweets have been around the Haystack community, NLP and GPT. They've
                                                                    been posting in English, and have had a positive, informative tone.
                                                                    
                                                                    Twitter stream: I've directed my team to set sharper rules on how we deal with unidentified objects.\n\nWe will inventory, improve ca… 
                                                                    the incursion by China’s high-altitude balloon, we enhanced radar to pick up slower objects.\n \nBy doing so, w…
                                                                    I gave an update on the United States’ response to recent aerial objects. 

                                                                    Summary: This user has lately been tweeting about having sharper rules to deal with unidentified objects and an incursuin by China's high-altitude
                                                                    baloon. Their tweets have mostly been neutral but determined in tone. They mostly post in English.

                                                                    Twitter stream: $tweets 
                                                                    
                                                                    Summary: 
                                                                    """)

    st.session_state["haystack_started"] = True                                                     
    return prompt_node, twitter_template


@st.cache(hash_funcs={"builtins.CoreBPE": lambda _: None}, show_spinner=False, allow_output_mutation=True)
def query(username, prompter, template):

    bearer_token = TWITTER_BEARER

    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = f"https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={username}&count={60}"
    try:
        response = requests.request("GET", url, headers = headers)
        twitter_stream = ""
        for tweet in response.json():
            twitter_stream += tweet["text"]
        result = prompter.prompt(prompt_template=template, tweets=twitter_stream)
    except Exception as e:
        print(e)
        result = ["Please make sure you are providing a correct, public twitter account"]
    return result