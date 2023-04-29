import lightbulb
import hikari
import ujson

from bombunia_manager import Bombunia

plugin = lightbulb.Plugin("get_grades")


@plugin.command
@lightbulb.command("raw", "Returns raw data. (json)")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def raw(ctx: lightbulb.Context) -> None:
    await ctx.respond("Ussage: `/raw grades` or `/raw last_grades`")


@raw.child
@lightbulb.add_cooldown(10, 1, lightbulb.GuildBucket)
@lightbulb.command("grades", "Returns newest grades.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def grades(ctx: lightbulb.Context) -> None:
    bmb = ctx.bot.d["bombunia"]

    x = bmb.get_grades(id_okres=1048)
    x = ujson.dumps(x, indent=4)

    with open("temp_newest_grades.json", "w") as f:
        f.write(x)

    f = hikari.File("temp_newest_grades.json", filename="newest_grades.json")

    await ctx.respond(f)


@raw.child
@lightbulb.command("last_grades", "Returns last grades.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def last_grades(ctx: lightbulb.Context) -> None:
    bmb = ctx.bot.d["bombunia"]

    x = bmb.get_last_grades()
    x = ujson.dumps(x, indent=4)

    with open("temp_last_grades.json", "w") as f:
        f.write(x)

    f = hikari.File("temp_last_grades.json", filename="last_grades.json")

    await ctx.respond(f)


def load(bot):
    bot.add_plugin(plugin)
