import os
from swarms import OpenAIChat, Agent, AgentRearrange
from dotenv import load_dotenv

load_dotenv()

# Load API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Define the model to be used
model = OpenAIChat(
    model_name="gpt-4o-mini", openai_api_key=api_key, max_tokens=4000, temperature=0.1
)

# Generator Agent - generates the core post
post_generator_agent = Agent(
    agent_name="Post-Generator-Agent",
    description="Generates core social media posts to promote GPTuesday's weekly AI events and workshops.",
    system_prompt="""
    Your task is to generate an engaging, clear, and informative post to promote GPTuesday's weekly AI educational events and community. Include the following platforms and event links:
    
    • Telegram: https://t.me/+w7NqSJA2WmgxMzdh
    • Discord: https://discord.gg/F8sSH4Gh
    • Twitter: https://twitter.com/GPTuesdays
    • Instagram: https://www.instagram.com/gptuesdays
    • LinkedIn: https://www.linkedin.com/company/gptuesdays
    • YouTube: https://www.youtube.com/@GPTuesdays
    • Website: https://gptuesdays.com/
    • Luma: https://lu.ma/GPTuesdays
    
    The tone should be professional yet friendly, encouraging people to join the events and connect on social platforms.
    """,
    llm=model,
    max_loops=1,
    dashboard=False,
    stopping_token="<DONE>",
)

# Telegram Optimizer Agent
telegram_optimizer_agent = Agent(
    agent_name="Telegram-Optimizer-Agent",
    description="Optimizes posts for the casual and conversational tone of Telegram.",
    system_prompt="""
    Your task is to optimize the given post for Telegram. Telegram posts should be informal and community-oriented. Use conversational language and encourage users to join the community.
    
    Example:
    "🚀 Join us for GPTuesday's weekly AI events and workshops! Explore the latest in AI, meet other enthusiasts, and learn something new. Join the chat: [Telegram link]."
    """,
    llm=model,
    max_loops=1,
    dashboard=False,
    stopping_token="<DONE>",
)

# Discord Optimizer Agent
discord_optimizer_agent = Agent(
    agent_name="Discord-Optimizer-Agent",
    description="Optimizes posts for the vibrant and community-driven nature of Discord.",
    system_prompt="""
    Your task is to optimize the post for Discord. Keep it short, fun, and engaging, and be sure to encourage conversation and participation in the Discord server.
    
    Example:
    "🎉 Get ready for GPTuesday's AI events! We're hosting weekly workshops and discussions. Connect with fellow AI enthusiasts and expand your knowledge. Join the server: [Discord link]."
    """,
    llm=model,
    max_loops=1,
    dashboard=False,
    stopping_token="<DONE>",
)

# Twitter Optimizer Agent
twitter_optimizer_agent = Agent(
    agent_name="Twitter-Optimizer-Agent",
    description="Optimizes posts for Twitter, ensuring concise and engaging messaging.",
    system_prompt="""
    Your task is to optimize the post for Twitter. Ensure that it is brief, uses clear language, and includes a call to action. Limit to 280 characters.
    
    Example:
    "🚀 Join GPTuesday for weekly AI workshops & events in Miami! Connect with the AI community and learn the latest trends. Follow us: [Twitter link] #AI #GPTuesday"
    """,
    llm=model,
    max_loops=1,
    dashboard=False,
    stopping_token="<DONE>",
)

# Instagram Optimizer Agent
instagram_optimizer_agent = Agent(
    agent_name="Instagram-Optimizer-Agent",
    description="Optimizes posts for Instagram, with a focus on visual engagement and concise messaging.",
    system_prompt="""
    Your task is to optimize the post for Instagram. Use engaging language, encourage visual engagement, and suggest using event photos or graphics. Ensure a clear call to action.
    
    Example:
    "📸 Join us every week for AI events in Miami with GPTuesday! Expand your skills, network with others, and explore the future of AI. Check out our upcoming events: [Instagram link]."
    """,
    llm=model,
    max_loops=1,
    dashboard=False,
    stopping_token="<DONE>",
)

# LinkedIn Optimizer Agent
linkedin_optimizer_agent = Agent(
    agent_name="LinkedIn-Optimizer-Agent",
    description="Optimizes posts for the professional tone of LinkedIn.",
    system_prompt="""
    Your task is to optimize the post for LinkedIn. Focus on a professional tone, highlighting networking opportunities and skill development. Encourage sign-ups and participation.
    
    Example:
    "🌟 Expand your AI knowledge with GPTuesday's weekly workshops and events. Engage with AI professionals, network, and enhance your skills. Sign up for upcoming events here: [LinkedIn link]."
    """,
    llm=model,
    max_loops=1,
    dashboard=False,
    stopping_token="<DONE>",
)

# YouTube Optimizer Agent
youtube_optimizer_agent = Agent(
    agent_name="YouTube-Optimizer-Agent",
    description="Optimizes posts for YouTube, ensuring a focus on video content and event highlights.",
    system_prompt="""
    Your task is to optimize the post for YouTube. Emphasize the value of video content, such as event highlights or tutorials, and encourage subscriptions.
    
    Example:
    "🎥 Want to dive deeper into AI? Check out GPTuesday's weekly workshops and event highlights on our YouTube channel. Subscribe for more insights and tutorials: [YouTube link]."
    """,
    llm=model,
    max_loops=1,
    dashboard=False,
    stopping_token="<DONE>",
)

# Website Optimizer Agent
website_optimizer_agent = Agent(
    agent_name="Website-Optimizer-Agent",
    description="Optimizes posts for the GPTuesday website, ensuring clarity and engagement.",
    system_prompt="""
    Your task is to optimize the post for the website. The content should be clear, informative, and engaging, ensuring users can easily find event details and sign-up links.
    
    Example:
    "🚀 GPTuesday hosts weekly AI workshops and events in Miami. Join us to explore the latest in AI technology, network with others, and build your skills. Check out our upcoming events here: [Website link]."
    """,
    llm=model,
    max_loops=1,
    dashboard=False,
    stopping_token="<DONE>",
)

# List of agents
agents = [
    post_generator_agent,
    telegram_optimizer_agent,
    discord_optimizer_agent,
    twitter_optimizer_agent,
    instagram_optimizer_agent,
    linkedin_optimizer_agent,
    youtube_optimizer_agent,
    website_optimizer_agent,
]

swarm = AgentRearrange(
    agents=agents,
    flow="Post-Generator-Agent -> Telegram-Optimizer-Agent, Discord-Optimizer-Agent, Twitter-Optimizer-Agent, Instagram-Optimizer-Agent, LinkedIn-Optimizer-Agent, YouTube-Optimizer-Agent, Website-Optimizer-Agent",
    # return_json=True,
)


swarm.run(
    "Create posts to advertise the upcoming GPTuesday event on November 2nd at 6pm in Little Havana."
)
