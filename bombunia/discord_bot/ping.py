import lightbulb

plugin = lightbulb.Plugin("ping")

@plugin.command
@lightbulb.command('ping', 'Returns pong, and the latency of the bot')
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"Pong! {ctx.bot.heartbeat_latency * 1000:.0f}ms")

def load(bot):
    bot.add_plugin(plugin)