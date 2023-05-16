import lightbulb
import hikari
import ujson
import datetime

from bombunia_manager import Bombunia
from analyzer import Analyzer

from PIL import Image

plugin = lightbulb.Plugin("graph")

@plugin.command
@lightbulb.command("graph", "Returns data represented in graphical form.")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def graph(ctx: lightbulb.Context) -> None:
    await ctx.respond("Ussage: `/graph grades` or `/graph last_two`")

@graph.child
@lightbulb.add_cooldown(10, 1, lightbulb.GuildBucket)
@lightbulb.option("start_date", "Start date of the graph.", type=str,required=True)
@lightbulb.option("end_date", "End date of the graph.", type=str,required=False)
@lightbulb.command("grades_date", "(YYYY-MM-DD) Returns graph for specified time period.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def grades_date(ctx: lightbulb.Context) -> None:
    bmb = ctx.bot.d["bombunia"]
    an = Analyzer()
    _p = []

    _end_date = datetime.datetime.now()

    if ctx.options.end_date is not None:
        _end_date = datetime.datetime.strptime(ctx.options.end_date, "%Y-%m-%d")

    _start_date = datetime.datetime.strptime(ctx.options.start_date, "%Y-%m-%d")
    
    _x = bmb.get_all_grades()

    for i in _x:
        if datetime.datetime.fromtimestamp(i[0]["time"]) >= _start_date and datetime.datetime.fromtimestamp(i[0]["time"]) <= _end_date:
            _p.append(i)

    _x = an.graph_from_list(_p)

    _x.save("temp_graph.png")

    f = hikari.File("temp_graph.png", filename="graph.png")

    await ctx.respond(f)


@graph.child
@lightbulb.add_cooldown(10, 1, lightbulb.GuildBucket)
@lightbulb.command("grades", "Returns graph of all grades.")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def grades(ctx: lightbulb.Context) -> None:
    bmb = ctx.bot.d["bombunia"]
    an = Analyzer()

    # x = bmb.get_all_grades()

    # print(x[0])
    # print()
    # print(x[len(x)-1])

    # d = bmb.compare_grades(x[0],x[len(x)-1],save_grades_a=False)

    # x = an.graph_from_list(x[len(x)-1])

    _x = bmb.get_all_grades()

    _x = an.graph_from_list(_x)

    _x.save("temp_graph.png")

    # with open("temp_graph.png", "wb") as f:
    #     f.write(_x)

    f = hikari.File("temp_graph.png", filename="graph.png")

    await ctx.respond(f)

def load(bot):
    bot.add_plugin(plugin)