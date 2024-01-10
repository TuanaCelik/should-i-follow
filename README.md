---
title: Should I follow?
emoji: 🦄
colorFrom: pink
colorTo: yellow
sdk: streamlit
sdk_version: 1.21.0
app_file: app.py
pinned: false
---


# Should I Follow?

### Try it out on [🤗 Spaces](https://huggingface.co/spaces/deepset/should-i-follow)

##### A simple app to get an overview of what the Mastodon user has been posting about and their tone

This is a demo just for fun 🥳
This repo contains a streamlit application that given a Mastodon username, tells you what type of things they've been posting about lately, their tone, and the languages they use. It uses the LLM by OpenAI `gpt-4`.

It's been built with [Haystack](https://haystack.deepset.ai) using the [`OpenAIGenerator`](https://docs.haystack.deepset.ai/v2.0/docs/openaigenerator) and by creating a [`PromptBuilder`](https://docs.haystack.deepset.ai/v2.0/docs/promptbuilder)

https://user-images.githubusercontent.com/15802862/220464834-f42c038d-54b4-4d5e-8d59-30d95143b616.mov


### Points of improvement

Since we're using a generative model here, we need to be a bit creative with the prompt we provide it to minimize any hallucination or similar unwanted results. For this reason, I've tried to be a bit creative with the `PromptBuilder` template and give some examples of _how_ to construct a summary. However, this still sometimes produces odd results.

If you try to run it yourself and find ways to make this app better, please feel free to create an issue/PR 🙌

## To learn more about the PromptBuilder

As of Haystack 2.0-Beta onwards, you can create prompt templates with Jinja. Check out guide on creating prompts [here](https://docs.haystack.deepset.ai/v2.0/docs/promptbuilder)

## Installation and Running
To run the bare application which does _nothing_:
1. Install requirements:
`pip install -r requirements.txt`
2. Run the streamlit app:
`streamlit run app.py`

This will start up the app on `localhost:8501` where you will dind a simple search bar

#### The Haystack Community is on [Discord](https://discord.com/invite/VBpFzsgRVF)
