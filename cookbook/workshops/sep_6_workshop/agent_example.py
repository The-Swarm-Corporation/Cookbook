import os
from swarms import OpenAIChat, Agent
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
# .env OPENAI_API_KEY="sk-"

model = OpenAIChat(
    model_name="gpt-4o-mini", openai_api_key=api_key, max_tokens=4000, temperature=0.1
)


agent = Agent(
    agent_name="Financial-Advisor-Agent",
    description="Your task is to provide financial advice to clients. You will help them with their financial planning, investment strategies, and retirement planning. You will also provide advice on tax planning, estate planning, and insurance planning. You will need to understand the client's financial goals, risk tolerance, and investment preferences to provide the best advice. You will need to stay up-to-date on the latest financial products, market trends, and regulations to provide the best advice to your clients.",
    system_prompt="",
    llm=model,
    max_loops=1,
    dashboard=False,
    stopping_token="<DONE>",
)


# Run the agent
out = agent.run("What are interesting ways to deduct taxes for a small business?")
print(out)
