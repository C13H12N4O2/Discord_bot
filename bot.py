import lol
import music
import utils
from discord.ext import commands

bot = commands.Bot(command_prefix=['후추 ', '후추얘 '], description='광견 후추 봇입니다.')

@bot.event
async def on_ready():
    utils.print_log('warning', f'{bot.user} has connected to Discord!')
    async for guild in bot.fetch_guilds():
        utils.print_log('warning', f'{guild.name}[{guild.id}]')
    bot.add_cog(lol.LOL(bot))
    bot.add_cog(music.Music(bot))

    
def main():
    bot.run(utils.get_env_info('DISCORD_TOKEN'))
    
if __name__ == '__main__':
    main()
