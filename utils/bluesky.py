from typing import List

import requests
from haystack import Document, component


@component
class BlueskyFetcher:
    @component.output_types(documents=List[Document])
    def run(self, username: str, last_k_posts: int = 20):
        username = username.lstrip("@")
        url = (
            f"https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed"
            f"?actor={username}&limit={last_k_posts}"
        )
        response = requests.get(url)
        response.raise_for_status()

        documents = []
        for item in response.json().get("feed", []):
            text = item.get("post", {}).get("record", {}).get("text", "")
            if text:
                documents.append(Document(content=text))
        return {"documents": documents}
