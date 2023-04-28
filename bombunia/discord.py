import hikari
import lightbulb

from utils import load_cfg
from bombunia_manager import Bombunia
from analyzer import Analyzer

import logging

__logger = logging.getLogger("Bombunia")
__logger.addHandler(logging.NullHandler())

cfg = load_cfg()


bot = lightbulb.BotApp(
    token=cfg["discord"]["token"],
    prefix=cfg["discord"]["prefix"],
)


@bot.listen()
async def on_ready(event: hikari.StartingEvent) -> None:
    __logger.info(f"Bot is now ready!")

    bot.d["bombunia"] = Bombunia(
        username=cfg["vulcan"]["username"],
        password=cfg["vulcan"]["password"],
        cookies={},
        school_url=cfg["vulcan"]["school_url"],
        school_alias=cfg["vulcan"]["school_alias"],
        symbol=cfg["vulcan"]["symbol"],
        school_pupil_url=cfg["vulcan"]["school_pupil_url"],
    )

    bmb = bot.d["bombunia"]

    x = bmb.init_session()
    bmb.close_session()

    bmb.symbol = x["symbol"]
    bmb.cookies = x["cookies"]
    bmb.school_pupil_url = f"{bmb.school_pupil_url}{bmb.school_alias}/{bmb.symbol}/Statystyki.mvc/GetOcenyCzastkowe"

    await bot.update_presence(
        activity=hikari.Activity(name=f"🅱️ Bombunia v{cfg['version']}")
    )


if __name__ == "__main__":
    bot.load_extensions_from("./discord_bot")
    bot.run()

# @bot.listen()

# @bot.

# async def on_message_create(event: hikari.MessageCreateEvent) -> None:
#     if not event.is_human or not event.content:
#         return

#     me = bot.get_me()
#     if not me:
#         return

#     if event.content == f"<@{me.id}>":
#         await event.message.respond(f"🅱️ Bombunia v{cfg['version']} - {bot.heartbeat_latency * 1000:.0f}ms")

# if __name__ == "__main__":
#     bot.run()
