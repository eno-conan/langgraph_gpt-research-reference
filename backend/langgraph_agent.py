import os
import time
from concurrent.futures import ThreadPoolExecutor
from langgraph.graph import Graph
# 画像
from IPython.display import Image

# Import agent classes
from .agents import SearchAgent, CuratorAgent, WriterAgent, DesignerAgent, EditorAgent, PublisherAgent, CritiqueAgent


class MasterAgent:
    def __init__(self):
        pass
        # self.output_dir = f"outputs/run_{int(time.time())}"
        # os.makedirs(self.output_dir, exist_ok=True)

    # def run(self, queries: list):
    def run(self, queries: list, layout: str):
        # Initialize agents
        search_agent = SearchAgent()
        curator_agent = CuratorAgent()
        writer_agent = WriterAgent()
        # critique_agent = CritiqueAgent()
        # designer_agent = DesignerAgent(self.output_dir)
        # editor_agent = EditorAgent(layout)
        # publisher_agent = PublisherAgent(self.output_dir)

        # Define a Langchain graph
        workflow = Graph()

        # Add nodes for each agent
        workflow.add_node("search", search_agent.run)
        workflow.add_node("curate", curator_agent.run)
        workflow.add_node("write", writer_agent.run)
        # workflow.add_node("critique", critique_agent.run)
        # workflow.add_node("design", designer_agent.run)

        # Set up edges
        # searchからcurateに向けた矢印
        workflow.add_edge('search', 'curate')
        workflow.add_edge('curate', 'write')
        # workflow.add_edge('write', 'critique')
        # writeからcritiqueについて、条件を満たす（accept）なら、critique
        # https://blog.langchain.dev/reflection-agents/
        # workflow.add_conditional_edges(start_key='critique',
        #                                condition=lambda x: "accept" if x['critique'] is None else "revise",
        #                                # acceptなら、どのnodeに、reviseならどのnodeに進むか
        #                                conditional_edge_mapping={"accept": "design", "revise": "write"})

        # # set up start and end nodes（スタートとゴールの決定）
        workflow.set_entry_point("search")
        # workflow.set_finish_point("curate")
        workflow.set_finish_point("write")
        # workflow.set_finish_point("design")

        # compile the graph
        chain = workflow.compile()
        
        # graph図示
        chain.get_graph().print_ascii()
        # https://zenn.dev/wakachikooo/articles/1934ec3006e9bf
        # https://github.com/langchain-ai/langgraph/issues/69
        # https://github.com/langchain-ai/langgraph/blob/main/examples/rag/langgraph_crag.ipynb?ref=blog.langchain.dev
        # Colabじゃないとだめ？
        # Image(chain.get_graph().draw_png())

        # Execute the graph for each query in parallel
        with ThreadPoolExecutor() as executor:
            parallel_results = list(executor.map(lambda q: chain.invoke({"query": q}), queries))
            
        return parallel_results
        # Compile the final newspaper
        # newspaper_html = editor_agent.run(parallel_results)
        # newspaper_path = publisher_agent.run(newspaper_html)

        # return newspaper_path
