from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession
import os

# ... (Your existing code)

# Event handler for old messages
async def forward_old_messages():
    # Call the print_entities function
    await print_entities()

    destination_channels = TO  # Assuming TO_ contains a comma-separated list of channel IDs
    for channel_id in destination_channels.split(','):
        try:
            destination_channel = await steallootdealUser.get_entity(int(channel_id))

            async for message in steallootdealUser.iter_messages(FROM_):
                await forward_messages(message, destination_channel)

        except ValueError as ve:
            print(f"Error: {ve}. Check if the channel ID {channel_id} is correct.")
        except Exception as e:
            print(f"Error forwarding old messages to channel {channel_id}: {e}")

# Add this function for debugging
async def print_entities():
    dialogs = await steallootdealUser.get_dialogs()
    for dialog in dialogs:
        print(f"{dialog.name}: {dialog.id}")

# Run the bot
print("Bot has started.")

# Create an event loop and run the forward_old_messages function
import asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(forward_old_messages())

# Start the event loop for handling new messages
steallootdealUser.run_until_disconnected()
