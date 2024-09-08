import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch bot token and channel ID from environment variables
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")

DISCORD_API_URL = "https://discord.com/api/v10"


def send_discord_message(message: str) -> None:
    """
    Sends a message to a Discord channel using Discord's HTTP API.

    Args:
        message (str): The message to send to the Discord channel.

    Raises:
        ValueError: If the channel ID or message is invalid.
        requests.exceptions.RequestException: If an issue occurs while making the HTTP request.
    """
    if not TOKEN:
        raise ValueError("Discord bot token is not set in the .env file.")
    if not CHANNEL_ID:
        raise ValueError("Discord channel ID is not set in the .env file.")
    if not message:
        raise ValueError("Message cannot be empty.")

    url = f"{DISCORD_API_URL}/channels/{CHANNEL_ID}/messages"
    headers = {"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"}
    payload = {"content": message}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        print(f"Message sent: {message}")
    except requests.exceptions.RequestException as e:
        print(f"RequestException: {e}")
        raise


# Example usage:
if __name__ == "__main__":
    try:
        send_discord_message("Hello, this is a synchronous message from my bot!")
    except Exception as e:
        print(f"Error: {e}")
