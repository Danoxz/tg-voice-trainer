from telethon import TelegramClient, events
from dotenv import load_dotenv
import logging
import os

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
whitelist = set(map(int, os.getenv('WHITELIST', '').split(',')))

# The boundary between those messages that will be deleted and those that will not be
long_message_split = 15

client = TelegramClient('voice_trainer', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def handle_message(event):
    if (not event.is_private) or (not event.message.voice):
        return

    sender = await event.get_sender()
    sender_id = sender.id

    # Get sender name
    if hasattr(sender, 'username') and sender.username:
        sender_name = f"@{sender.username}"
    elif hasattr(sender, 'first_name') and sender.first_name:
        sender_name = sender.first_name
    else:
        sender_name = "Unknown"

    if sender_id in whitelist:
        logger.info(f"Message from whitelisted user {sender_name}. Skipping.")
        return
    
    message_time = event.message.date.strftime("%Y-%m-%d %H:%M:%S")

    voice_duration = event.message.voice.attributes[0].duration

    if voice_duration >= long_message_split:
        logger.info(f"Long voice received from {sender_name} ({sender_id}) at {message_time}. Duration: {voice_duration} seconds")
        return

    logger.info(f"Short voice received from {sender_name} ({sender_id}) at {message_time}. Duration: {voice_duration} seconds")
    
    # Delete and reply
    try:        
        await event.reply("Это автоответчик\nПривет! Может стоит написать текстом?")
        logger.info(f"Replied to voice from {sender_name} ({sender_id}) at {message_time}")

        await event.message.delete()
        logger.info(f"Deleted voice from {sender_name} ({sender_id}) at {message_time}")
    except Exception as e:
        logger.error(f"Error deleting or replying to voice message from {sender_name} ({sender_id}) at {message_time}: {e}")

def say_hello(): # its rofls
    print('''                                                                                 ''')
    print('''                            *   )                                      )      )  ''')
    print(''' (   (     (          (   ` )  /( (       )  (            (   (     ( /(   ( /(  ''')
    print(''' )\  )\ (  )\   (    ))\   ( )(_)))(   ( /(  )\   (      ))\  )(    )\())  )\()) ''')
    print('''((_)((_))\((_)  )\  /((_) (_(_())(()\  )(_))((_)  )\ )  /((_)(()\  ((_)\  ((_)\  ''')
    print('''\ \ / /((_)(_) ((_)(_))   |_   _| ((_)((_)_  (_) _(_/( (_))   ((_)  / (_) /  (_) ''')
    print(''' \ V // _ \| |/ _| / -_)    | |  | '_|/ _` | | || ' \))/ -_) | '_|  | | _| () |  ''')
    print('''  \_/ \___/|_|\__| \___|    |_|  |_|  \__,_| |_||_||_| \___| |_|    |_|(_)\__/   ''')
    print('''                                                                                 ''')

async def main():
    await client.start()
    logger.info("Client started")
    say_hello()
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
