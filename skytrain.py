from pyrogram import Client, filters
import asyncio

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
    "/spe": "Team 8",
    "/spd": "Team 7",
    "/def": "Team 6",
    "/spa": "Team 5",
    "/atk": "Team 4"
}


async def train_function(client, message):
    text = message.text or message.caption or ""
    print(text)

    if text.startswith("/"):
        command = text.split()[0].lower()

        if command in button_names:
            button = button_names[command]

            msg = await client.get_messages(
                BOT_USER,
                TEAM_MESSAGE_ID
            )

            if not msg or not msg.reply_markup:
                print("Team keyboard not found")
                return

            try:
                await msg.click(button)
                print(f"Clicked {button}")
                await message.reply(
    f"**⦿ {button_names[command]} 〔{text.replace('/', '').upper()}〕**\n"
    f"Send a challenge to proceed."
)
            except Exception as e:
                print(f"Failed to click {button}: {e}")

            return

    if (
        "80085" in text
        and any(word in text for word in ["challenges", "Current turn: 80085", "80085's Pokemon fainted!"])
        and message.reply_markup
    ):
        print("clicked")
        print(text)

        sleep_time = 3 if "fainted" in text.lower() else 1.5

        await asyncio.sleep(sleep_time)
        await message.click(0)


@app.on_message(
    filters.chat(CHAT_ID)
    & filters.command(["exp", "hp", "spe", "spd", "def", "spa", "atk"])
)
async def command_handler(client, message):
    await train_function(client, message)


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


app.run()