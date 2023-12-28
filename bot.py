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

BLOCKED_TEXTS = config("BLOCKED_TEXTS", default="", cast=lambda x: [i.strip().lower() for i in x.split(',')])
MEDIA_FORWARD_RESPONSE = config("MEDIA_FORWARD_RESPONSE", default="yes").lower()

YOUR_ADMIN_USER_ID = config("YOUR_ADMIN_USER_ID", default=0, cast=int)
BOT_API_KEY = config("BOT_API_KEY", default="", cast=str)

# Initialize Telethon client
try:
    steallootdealUser = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    steallootdealUser.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

async def forward_messages(event):
    for channel_id in TO_CHANNEL.split(','):
        try:
            destination_channel = await steallootdealUser.get_entity(int(channel_id))

            message_text = event.raw_text.lower()

            if any(blocked_text in message_text for blocked_text in BLOCKED_TEXTS):
                print(f"Blocked message containing one of the specified texts: {event.raw_text}")
                logging.warning(f"Blocked message containing one of the specified texts: {event.raw_text}")
                continue

            if event.media:
                user_response = MEDIA_FORWARD_RESPONSE
                if user_response != 'yes':
                    print(f"Media forwarding skipped by user for message: {event.raw_text}")
                    continue

                await steallootdealUser.send_message(destination_channel, message_text, file=event.media)
                print(f"Forwarded media message to channel {channel_id}")

            else:
                await steallootdealUser.send_message(destination_channel, message_text)
                print(f"Forwarded text message to channel {channel_id}")

        except ValueError as ve:
            print(f"Error: {ve}. Check if the channel ID {channel_id} is correct.")
        except Exception as e:
            print(f"Error forwarding message to channel {channel_id}: {e}")

# Event handler for incoming messages
@steallootdealUser.on(events.NewMessage(incoming=True, chats=FROM_CHANNEL))
async def handle_incoming_messages(event):
    await forward_messages(event)

# Event handler for old messages
async def forward_old_messages():
    async for message in steallootdealUser.get_messages(FROM_CHANNEL):
        await forward_messages(message)

# Run the bot
print("Bot has started.")

# Create an event loop and run the forward_old_messages function
import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(forward_old_messages())

# Start the event loop for handling new messages
steallootdealUser.run_until_disconnected()
