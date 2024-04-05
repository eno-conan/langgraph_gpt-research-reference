from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


class SearchAgent:
    def __init__(self):
        pass

    def search_tavily(self, query: str):
        #  https://docs.tavily.com/docs/tavily-api/python-sdk#usage-%EF%B8%8F
        # https://docs.tavily.com/docs/tavily-api/Topics/news
        results = tavily_client.search(query=query, \
                                       topic="news", \
                                       max_results=10, \
                                       search_depth="advanced", \
                                       include_images=True)
        sources = results['results']
        print(sources)
        try:
            image = results["images"][0]
        except:
            image = "https://images.unsplash.com/photo-1542281286-9e0a16bb7366?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8bmV3c3BhcGVyJTIwbmV3c3BhcGVyJTIwYXJ0aWNsZXxlbnwwfHwwfHw%3D&ixlib=rb-1.2.1&w=1000&q=80"
        return sources, image

    def run(self, article: dict):
        res = self.search_tavily(article["query"])
        article["sources"] = res[0]
        article["image"] = res[1]
        return article
