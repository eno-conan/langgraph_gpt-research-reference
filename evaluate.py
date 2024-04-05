from langsmith import Client
from langsmith.schemas import Run, Example
from langsmith.evaluation import evaluate
import openai
from langsmith.wrappers import wrap_openai
# 
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

client = Client()

# Define dataset: these are your test cases
# とりあえず、データセットを用意する。
dataset_name = "Rap Battle Dataset2"
dataset = client.create_dataset(dataset_name, description="Rap battle prompts.")
client.create_examples(
    inputs=[
        {"question": "a rap battle between Atticus Finch and Cicero"},
        {"question": "a rap battle between Barbie and Oppenheimer"},
    ],
    outputs=[
        {"must_mention": ["lawyer", "justice"]},
        {"must_mention": ["plastic", "nuclear"]},
    ],
    dataset_id=dataset.id,
)

# Define AI system
# Patch the OpenAI client to make it traceable.
openai_client = wrap_openai(openai.Client())

# ここが作業によって変わってくる、ってことか？
def predict(inputs: dict) -> dict:
    messages = [{"role": "user", "content": inputs["question"]}]
    response = openai_client.chat.completions.create(messages=messages, model="gpt-3.5-turbo")
    return {"output": response}

# Define evaluators
# 評価方法の定義
def must_mention(run: Run, example: Example) -> dict:
    prediction = run.outputs.get("output") or ""
    required = example.outputs.get("must_mention") or []
    # predictionの全ての要素がrequiredの全ての要素を含んでいるかどうか
    # TrueかFalseが返されることになる
    score = all(phrase in prediction for phrase in required)
    return {"key":"must_mention", "score": score}

experiment_results = evaluate(
    predict, # Your AI system
    data=dataset_name, # The data to predict and grade over
    # The evaluators to score the results
    # 配列、ってことは複数の評価方法を設定可能ということか。
    evaluators=[must_mention], 
    experiment_prefix="custom-rap-generator",
    metadata={
      "version": "1.0.0",
    },
)