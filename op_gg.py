import cloudscraper
from bs4 import BeautifulSoup as bs

class OP_GG():
    def __init__(self, **requests_kwargs):
        self.s = cloudscraper.create_scraper()
        self.requests_kwargs = requests_kwargs
        self.host = 'http://www.op.gg'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36',
            'referer': 'http://www.op.gg/'
        }
        
    def parse_url(self, url, mode='get', headers=None, data=None, params=None, stream=False):
        if not headers:
            headers = self.headers
        if mode == 'get':
            return self.s.get(url, headers=headers, data=data, params=params, stream=stream, **self.requests_kwargs)
        if mode == 'post':
            return self.s.post(url, headers=headers, data=data, params=params, stream=stream, **self.requests_kwargs)
        if mode == 'delete':
            return self.s.delete(url, headers=headers, data=data, params=params, stream=stream, **self.requests_kwargs)
            
    def soup_response(self, response):
        return bs(response, 'html.parser')
        
    def summoner_detail(self, user_name):
        return f'{self.host}/summoner/{user_name}'

    def main_icon(self):
        res = self.parse_url(self.host)
        html = self.soup_response(res.text).find('div', {'id': 'logo'}).find('img')
        dict = {
            'title': html['title'],
            'src': html['src'],
            'alt': html['alt']
        }
        return dict
        
    def default_icon(self):
        return 'https://talk.op.gg/images/img-opgglogo@2x.png'
        
    def summoner_page(self, user_name, l='ko_KR'):
        url = f'{self.host}/summoner/'
        params = {
            'userName': user_name,
            'l': l
        }
        res = self.parse_url(url, params=params)
        return self.soup_response(res.text)
        
    def recent_match(self, user_name, l='ko_KR'):
        html = self.summoner_page(user_name, l)
        list = {}
        try:
            match_list = html.find('div', {'class': 'GameItemList'}).find_all('div', {'class': 'GameItemWrap'})
        except:
            return None
        index = 0
        for match in match_list[:3]:
            data = {
                'data-game-result': None,
                'GameType': None,
                'ChampionImage': None,
                'ChampionName': None,
                'total_cs': None,
                'GameLength': None
            }
            data['data-game-result'] = match.find('div')['data-game-result']
            data['GameType'] = match.find('div', {'class': 'GameType'})['title']
            data['ChampionImage'] = f'https:{match.find("div", {"class": "ChampionImage"}).find("img")["src"]}'
            data['ChampionName'] = match.find('div', {'class': 'ChampionImage'}).find('img')['alt']
            data['GameLength'] = str(match.find('div', {'class': 'GameLength'})).split('>')[-2].split('<')[0]
            KDA = str(match.find('div', {'class': 'KDA'}).find_all('span'))
            for kda_data in KDA.split(',')[:4]:
                data[kda_data.split('"')[1]] = kda_data.split('"')[-1].split('<')[0].split('>')[-1]
            CS = match.find('div', {'class': 'CS'}).find('span')['title'].split('<br>')
            total_cs = 0
            for cs_data in CS[0].split('  + '):
                total_cs += int(cs_data.split(' ')[-1])
            data['total_cs'] = str(total_cs)
            cpm = CS[-1].split(' ')
            data['cpm'] = float(cpm[-1].split('개')[0])
            list[index] = data
            index += 1
        return list
        
    def rank_info(self, user_name, l='ko_KR'):
        html = self.summoner_page(user_name, l)
        data = {
            'Name': None,
            'RankType': None,
            'TierRank': None,
            'LeaguePoints': None,
            'wins': None,
            'losses': None,
            'winratio': None
        }
        try:
            data['Name'] = str(html.find('div', {'class': 'Information'}).find_all('span', {'class': 'Name'})[-1]).split('>')[-2].split('<')[0]
        except:
            data['Name'] = str(html.find('div', {'class': 'Information'}).find('span', {'class': 'Name'})[-1]).split('>')[-2].split('<')[0]
        html = html.find('div', {'class': 'SummonerRatingMedium'})
        data['RankType'] = str(html.find('div', {'class': 'RankType'})).split('>')[-2].split('<')[0]
        try:
            data['TierRank'] = str(html.find('div', {'class': 'TierRank'})).split('>')[-2].split('<')[0].replace('\t', '').replace('\n', '')
        except:
            data['TierRank'] = str(html.find('div', {'class': 'TierRank'})).split('>')[-2].split('<')[0]
        try:
            data['LeaguePoints'] = str(html.find('span', {'class': 'LeaguePoints'})).split('>')[-2].split('<')[0].replace('\t', '').replace('\n', '')
        except:
            return data
        data['wins'] = str(html.find('span', {'class': 'wins'})).split('>')[-2].split('<')[0]
        data['losses'] = str(html.find('span', {'class': 'losses'})).split('>')[-2].split('<')[0]
        data['winratio'] = str(html.find('span', {'class': 'winratio'})).split('>')[-2].split('<')[0]
        return data
