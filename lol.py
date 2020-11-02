import op_gg
import utils
from discord.ext import commands

class LOL(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.opgg = op_gg.OP_GG()
        self.default_icon = self.opgg.default_icon()
        self.main_icon = self.opgg.main_icon()
        
    def get_game_result(self, game_result):
        result = {
            'data-game-result': '승리',
            'color': 0x00ff56
        }
        if game_result == 'lose':
            result['data-game-result'] = '패배'
            result['color'] = 0xE10000
        return result
    
    @commands.command(name='롤전적')
    async def _opgg(self, ctx, *, user_name):
        utils.print_log('warning', f'{ctx.author}[{ctx.author.id}]: {ctx.message.content}')
        user_name.replace(' ', '+')
        if not user_name:
            await ctx.send('소환사 이름을 입력해주세요.')
            return
        opgg_url = self.opgg.summoner_detail(user_name)
        user_info = self.opgg.rank_info(user_name)
        data = self.opgg.recent_match(user_name)
        if data:
            for index in range(0, 3):
                match_result = self.get_game_result(data[index]['data-game-result'])
                embed = utils.get_embed(f'{data[index]["ChampionName"]}', f'{data[index]["GameType"]}', match_result['color'])
                utils.set_embed(embed, 'author', name=f'{user_info["Name"]}의 전적', url=opgg_url, icon_url=self.default_icon)
                utils.set_embed(embed, 'set_thumbnail', url=data[index]['ChampionImage'])
                utils.set_embed(embed, 'add_field', name=f'{user_info["RankType"]}', value=f'{user_info["TierRank"]}')
                if user_info['winratio']:
                    utils.set_embed(embed, 'add_field', name=f'{user_info["LeaguePoints"]} {user_info["wins"]}  {user_info["losses"]}', value=f'{user_info["winratio"]}')
                utils.set_embed(embed, 'add_field', name=f'{match_result["data-game-result"]}', value=f'{data[index]["GameLength"]}')
                utils.set_embed(embed, 'add_field', name=f'KDA {data[index]["Kill"]}/{data[index]["Death"]}/{data[index]["Assist"]}', value=f'CS {data[index]["total_cs"]}({data[index]["cpm"]})')
                await ctx.send(embed=embed)
        else:
            await ctx.send('해당 소환사의 최근 전적이 존재하지않아요.')

    @commands.command(name='롤로고')
    async def _opgg_logo(self, ctx):
        embed = utils.get_embed(color=0x5c84e1)
        utils.set_embed(embed, 'set_thumbnail', url=self.main_icon['src'])
        await ctx.send(embed=embed)
