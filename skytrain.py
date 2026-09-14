from pyrogram import Client, filters
import asyncio
from flask import Flask
from threading import Thread

app = Client(
    "skytrain",
    api_id=2912653,
    api_hash="36a616c83fb35db05d768b40cd18242b"
)

BOT_USER = "PokepiaBot"
CHAT_ID = -1004265573604
TEAM_MESSAGE_ID = 1812

button_names = {
    "/exp": "Team 9",
    "/hp": "Team 9",
    "/speed": "Team 8",
    "/spdef": "Team 7",
    "/def": "Team 6",
    "/spatk": "Team 5",
    "/atk": "Team 4"
}

web = Flask(__name__)

@web.route("/")
def home():
    return "Skytrain is running"

@web.route("/health")
def health():
    return "OK"

def run_web():
    web.run(
        host="0.0.0.0",
        port=10000
    )


async def train_function(client, message):
    text = message.text or ""

    if "80085" in text and (
        "challenges" in text.lower()
        or "turn" in text.lower()
    ):
        if message.reply_markup:
            print("clicked")
            print(text)

            await asyncio.sleep(
                3 if "fainted" in text.lower() else 1.5
            )

            await message.click(0)


@app.on_message(
    filters.incoming
    & filters.user(BOT_USER)
    & filters.chat(CHAT_ID)
)
async def new_message(client, message):
    await train_function(client, message)


@app.on_edited_message(
    filters.incoming
    & filters.user(BOT_USER)
    & filters.chat(CHAT_ID)
)
async def edited_message(client, message):
    await train_function(client, message)


@app.on_message(
    filters.chat(CHAT_ID)
    & filters.command(
        ["exp", "hp", "speed", "spdef", "def", "spatk", "atk"]
    )
)
async def command_handler(client, message):
    command = message.text.split()[0].lower()

    if command not in button_names:
        return

    team_name = button_names[command]

    team_message = await client.get_messages(
        CHAT_ID,
        TEAM_MESSAGE_ID
    )

    if not team_message or not team_message.reply_markup:
        await message.reply("Team selection message not found.")
        return

    try:
        await team_message.click(team_name)

        await message.reply(
            f"**⦿ {team_name} selected**\n"
            f"Send a challenge to proceed."
        )

    except Exception as e:
        print(f"Button click failed: {e}")


Thread(
    target=run_web,
    daemon=True
).start()

app.run()
