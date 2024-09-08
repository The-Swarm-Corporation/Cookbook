from instagrapi import Client
from typing import List
import os


def send_instagram_dm(message: str, media_urls: List[str] = None) -> bool:
    """
    Sends a direct message to a user on Instagram.

    Args:
        username (str): The username of the recipient.
        message (str): The message to send in the DM.
        media_urls (List[str], optional): A list of URLs to media (images or videos) to send along with the message.

    Returns:
        bool: True if the DM was sent successfully, False otherwise.

    Raises:
        ValueError: If the username is invalid or the message is empty.
        Exception: If there is an issue with the Instagram API request.
    """
    client = Client()

    try:
        username = os.getenv("INSTAGRAM_USERNAME")
        password = os.getenv("INSTAGRAM_PASSWORD")
        # Log in to Instagram
        client.login(username, password)

        # Ensure the username and message are valid
        if not username:
            raise ValueError("The username cannot be empty.")
        if not message:
            raise ValueError("The message cannot be empty.")

        # Get the user ID for the recipient
        user_id = client.user_id_from_username(username)

        if media_urls:
            # Send a DM with media (images/videos)
            media_ids = [client.media_pk_from_url(url) for url in media_urls]
            client.direct_send(message, [user_id], media_pk=media_ids)
        else:
            # Send a simple text DM
            client.direct_send(message, [user_id])

        return True

    except ValueError as e:
        print(f"ValueError: {e}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        client.logout()
