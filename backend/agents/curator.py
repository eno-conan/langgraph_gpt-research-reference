from datetime import datetime
from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')


class CuratorAgent:
    def __init__(self):
        pass

    def curate_sources(self, query: str, sources: list):
        """
        Curate relevant sources for a query
        :param input:
        :return:
        """
        prompt = [{
            "role": "system",
            "content": "You are a personal newspaper editor. Your sole purpose is to choose 3 most relevant article "
                       "for me to read from a list of articles.\n "
        }, {
            "role": "user",
            "content": f"Today's date is {datetime.now().strftime('%d/%m/%Y')}\n."
                       f"Topic or Query: {query}\n"
                       f"query\n "
                       f"Here is a list of articles:\n"
                       f"{sources}\n"
        }]
        '''
        '''

        lc_messages = convert_openai_messages(prompt)
        print(lc_messages)
        # response = ChatOpenAI(model='gpt-4-0125-preview', max_retries=1).invoke(lc_messages).content
        response = ChatOpenAI(model='gpt-3.5-turbo-0125', max_retries=1).invoke(lc_messages).content
        chosen_sources = response
        for i in sources:
            if i["url"] not in chosen_sources:
                sources.remove(i)
        return sources

    def run(self, article: dict):
        article["sources"] = self.curate_sources(article["query"], article["sources"])
        return article
