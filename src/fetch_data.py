import os
import requests
from dotenv import load_dotenv
from src.utils import extract_name_tag


load_dotenv()
API_KEY = os.getenv('API_KEY')
LOL_VERSION = os.getenv('LOL_VERSION')


def get_riot_data(name, tag):
   """
   Fetches Riot data for a user using their name and tag.
   :param name:
   :param tag:
   :return:  {'puuid': 'a5RZqqIL_CxLSF9JQh9OrGPzQrnosMbU0K4gwsJkHMNZkSyYdFlMiZqt-WGeeMtfUUugFOLin99qXg', 'gameName': 'Thái Lê Tôn Giả', 'tagLine': '3110'}
   """
   url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={API_KEY}"
   response = requests.get(url)
   return response.json()




def get_id(name, tag):
   """
   Fetches the ID of a user using their name and tag. (summonerId)
   :param name:
   :param tag:
   :return: 8_WyYbdUxzIt0GJN_di-8M1UKrE0wMdbV7ZqPO2OtIygLntBRbPt78qMzQ
   """
   puuid = get_riot_data(name, tag)["puuid"]
   url = f"https://vn2.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={API_KEY}"
   response = requests.get(url).json()
   return response["id"]




def get_lol_data(name_with_tag: str):
   """
   Fetches League of Legends data for a user using their name and tag.
   :param name: Thái Lê Tôn Giả#3110
   :return:
   [
       {'queueType': 'CHERRY', 'summonerId': '8_WyYbdUxzIt0GJN_di-8M1UKrE0wMdbV7ZqPO2OtIygLntBRbPt78qMzQ', 'leaguePoints': 0, 'wins': 4, 'losses': 4, 'veteran': False, 'inactive': False, 'freshBlood': False, 'hotStreak': False},
       {'leagueId': '05b62fc9-97fa-49ab-b8a1-7cfe8a5e420d', 'queueType': 'RANKED_SOLO_5x5', 'tier': 'EMERALD', 'rank': 'I', 'summonerId': '8_WyYbdUxzIt0GJN_di-8M1UKrE0wMdbV7ZqPO2OtIygLntBRbPt78qMzQ', 'leaguePoints': 12, 'wins': 2, 'losses': 3, 'veteran': False, 'inactive': False, 'freshBlood': False, 'hotStreak': False},
       {'leagueId': '28afd3c1-5703-4a0c-830c-35f7906ee311', 'queueType': 'RANKED_FLEX_SR', 'tier': 'EMERALD', 'rank': 'II', 'summonerId': '8_WyYbdUxzIt0GJN_di-8M1UKrE0wMdbV7ZqPO2OtIygLntBRbPt78qMzQ', 'leaguePoints': 95, 'wins': 14, 'losses': 7, 'veteran': False, 'inactive': False, 'freshBlood': False, 'hotStreak': False}
   ]


   """
   name, tag = extract_name_tag(name_with_tag)
   summonerId = get_id(name, tag)
   url = f"https://vn2.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerId}?api_key={API_KEY}"
   response = requests.get(url).json()
   print("GET LOL DATA", response)
   return response


def get_match_data(name_with_tag):
   try:
       player_name, tag = extract_name_tag(name_with_tag)
       puuid = get_riot_data(player_name, tag)["puuid"]
       url = f"https://vn2.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}?api_key={API_KEY}"
       return requests.get(url).json()
   except Exception as e:
       print(e)






def get_champion_data_by_champion_id(champion_id: int):
   data = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{LOL_VERSION}/data/en_US/champion.json").json()
   champions = data["data"]
   for c_name, c in champions.items():
       if c["key"] == str(champion_id):
           return c["id"]
   return champion_id




if __name__ == '__main__':
   print(get_riot_data("Thái Lê Tôn Giả", "3110"))
   print(get_id("Thái Lê Tôn Giả", "3110"))
   print(get_lol_data("Thái Lê Tôn Giả", "3110"))
