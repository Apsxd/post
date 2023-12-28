from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession

# Configure logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

# Print starting message
print("Starting...")

# Read configuration from environment variables
APP_ID = config("APP_ID", default=0, cast=int)
API_HASH = config("API_HASH", default=None, cast=str)
SESSION = config("SESSION", default="", cast=str)
FROM_CHANNEL = config("FROM_CHANNEL", default="", cast=str)
TO_CHANNEL = config("TO_CHANNEL", default="", cast=str)

FROM = [int(i) for i in FROM_CHANNEL.split(',')]
TO = [int(i) for i in TO_CHANNEL.split(',')]

# Initialize Telethon client
try:
    steallootdealUser = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    steallootdealUser.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

# Event handler for incoming messages
@steallootdealUser.on(events.NewMessage(incoming=True, chats=FROM))
async def sender_bH(event):
    for i in TO:
        try:
            message_text = event.raw_text.lower()

            # Add your additional logic here, if needed

            if event.media:
                await steallootdealUser.send_message(i, message_text, file=event.media)
                print(f"Forwarded media message to channel {i}")
            else:
                await steallootdealUser.send_message(i, message_text)
                print(f"Forwarded text message to channel {i}")

        except Exception as e:
            print(f"Error forwarding message to channel {i}: {e}")

# Event handler for old messages
async def forward_old_messages():
    destination_channels = TO  # Assuming TO_CHANNEL contains a comma-separated list of channel IDs
    for channel_id in destination_channels:
        try:
            destination_channel = await steallootdealUser.get_entity(int(channel_id))

            async for message in steallootdealUser.iter_messages(FROM):
                message_text = message.raw_text.lower()

                # Add your additional logic here, if needed

                if message.media:
                    await steallootdealUser.send_message(destination_channel, message_text, file=message.media)
                    print(f"Forwarded old media message to channel {channel_id}")
                else:
                    await steallootdealUser.send_message(destination_channel, message_text)
                    print(f"Forwarded old text message to channel {channel_id}")

        except ValueError as ve:
            print(f"Error: {ve}. Check if the channel ID {channel_id} is correct.")
        except Exception as e:
            print(f"Error forwarding old messages to channel {channel_id}: {e}")

# Run the bot
print("Bot has started.")

# Create an event loop and run the forward_old_messages function
import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(forward_old_messages()

# Start the event loop for handling new messages
steallootdealUser.run_until_disconnected()
