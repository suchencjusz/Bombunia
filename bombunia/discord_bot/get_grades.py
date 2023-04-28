import lightbulb

from bombunia_manager import Bombunia

plugin = lightbulb.Plugin("get_grades")

@plugin.command
@lightbulb.command('get_grades', 'Returns latest grades, if there are any. Otherwise returns last grades.')
@lightbulb.implements(lightbulb.SlashCommand)
async def get_grades(ctx: lightbulb.Context) -> None:

    bmb = ctx.bot.d['bombunia']

    x = bmb.get_grades(id_okres=1048)

    await ctx.respond(x)

def load(bot):
    bot.add_plugin(plugin)