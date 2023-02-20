import streamlit as st
import requests
from utils.config import TWITTER_BEARER, OEPN_AI_KEY

from haystack.nodes import PromptNode, PromptTemplate

# cached to make index and models load only at start
@st.cache_resource
def start_haystack():
    #Use this function to contruct a pipeline
    prompt_node = PromptNode(model_name_or_path="text-davinci-003", api_key=OEPN_AI_KEY)

    twitter_template = PromptTemplate(name="twitter-voice", prompt_text="""You will be given a twitter stream belonging to a specific profile. Answer with a summary of what they've lately been tweeting about and in what languages.
                                                                    You may go into some detail about what topics they tend to like tweeting about. Please also mention their overall tone, for example: positive,
                                                                    negative, political, sarcastic or something else.

                                                                    Examples: 
                                                                    
                                                                    Twitter stream: Many people in our community asked how to utilize LLMs in their NLP pipelines and how to modify prompts for their tasks.…
                                                                    RT @deepset_ai: We use parts of news articles from The Guardian as documents and create custom prompt templates to categorize these article
                                                                    
                                                                    Summary: This person has lately been tweeting about NLP and LLMs. Their tweets have been in Enlish
                                                                    
                                                                    Twitter stream: I've directed my team to set sharper rules on how we deal with unidentified objects.\n\nWe will inventory, improve ca… 
                                                                    the incursion by China’s high-altitude balloon, we enhanced radar to pick up slower objects.\n \nBy doing so, w…
                                                                    I gave an update on the United States’ response to recent aerial objects. 

                                                                    Summary: This person has lately been tweeting about an unidentified object and an incursion by China with a high-altitude baloon.
                                                                    They have been tweeting about the USA. They have had a political tone. They mostly post in English.

                                                                    Twitter stream: $tweets 
                                                                    
                                                                    Summary: 
                                                                    """)
    return prompt_node, twitter_template

prompter, template = start_haystack()

@st.cache_data(show_spinner=False)
def query(username):

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
        result = ["Please make sure you are providing a correct, public twitter accout"]
    return result