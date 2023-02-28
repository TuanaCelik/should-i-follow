---
title: Should I follow?
emoji: 🦄
colorFrom: pink
colorTo: yellow
sdk: streamlit
sdk_version: 1.17.0
app_file: app.py
pinned: false
---


# Should I Follow?

### Try it out on [🤗 Spaces](https://huggingface.co/spaces/deepset/should-i-follow)

##### A simple app to get an overview of what the twitter user has been posting about and their tone

This is a demo just for fun 🥳
This repo contains a streamlit application that given a Twitter username, tells you what type of things they've been posting about lately, their tone, and the languages they use. It uses the LLM by OpenAI `text-davinci-003`.

It's been built with [Haystack](https://haystack.deepset.ai) using the [`PromptNode`](https://docs.haystack.deepset.ai/docs/prompt_node) and by creating a custom [`PromptTemplate`](https://docs.haystack.deepset.ai/docs/prompt_node#templates)

https://user-images.githubusercontent.com/15802862/220464834-f42c038d-54b4-4d5e-8d59-30d95143b616.mov


### Points of improvement

Since we're using a generative model here, we need to be a bit creative with the prompt we provide it to minimize any hallucination or similar unwanted results. For this reason, I've tried to be a bit creative with the `PromptTemplate` and give some examples of _how_ to construct a summary. However, this still sometimes produces odd results.

If you try to run it yourself and find ways to make this app better, please feel free to create an issue/PR 🙌

## To learn more about the PromptNode

Check out our tutorial on the PromptNode and how to create your own templates [here](https://haystack.deepset.ai/tutorials/21_customizing_promptnode)

## Installation and Running
To run the bare application which does _nothing_:
1. Install requirements:
`pip install -r requirements.txt`
2. Run the streamlit app:
`streamlit run app.py`
3. Createa a `.env` and add your Twitter Bearer token:
`TWITTER_BEARER_TOKEN` 

This will start up the app on `localhost:8501` where you will dind a simple search bar

#### The Haystack Community is on [Discord](https://discord.com/invite/VBpFzsgRVF)
