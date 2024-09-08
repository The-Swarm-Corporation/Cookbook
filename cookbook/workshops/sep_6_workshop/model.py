import os
from swarms import OpenAIChat
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
# .env OPENAI_API_KEY="sk-"

model = OpenAIChat(
    model_name="gpt-4o-mini", openai_api_key=api_key, max_tokens=4000, temperature=0.1
)

out = model(
    "How can I establish a ROTH IRA to buy stocks and get a tax break? What are the criteria"
)
print(out)
