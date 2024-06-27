import requests
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from src.fetch_data import get_match_data, get_champion_data_by_champion_id
from src.settings import *
from dotenv import load_dotenv
from threading import Thread

load_dotenv()
API_KEY = os.getenv('API_KEY')

class MatchData:
    def __init__(self, name_with_tag: str):
        self.team1 = []
        self.team2 = []
        background_path = "../img14.10.1/background/background_0.png"
        self.img = Image.open(background_path)
        enhancer = ImageEnhance.Brightness(self.img)
        # to reduce brightness by 50%, use factor 0.5
        self.img = enhancer.enhance(0.5)
        self.draw = ImageDraw.Draw(self.img)

        match_data = get_match_data(name_with_tag)
        if not match_data:
            print("Player or Match not found!")
        elif "status" in match_data.keys():
            print("Player or Match not found!")
        else:
            self.process_match_data(match_data)


    def process_match_data(self, match_data):
        participants = match_data["participants"]
        threads = []

        # Create threads for each player
        for player in participants:
            thread = Thread(target=self.process_player, args=(player,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        # for player in participants:
        #     team_id = player["teamId"]
        #     summoner_name = player["riotId"]
        #     summoner_id = player["summonerId"]
        #     champion_name = get_champion_data_by_champion_id(player["championId"])
        #
        #     solo_tier, solo_rank, flex_tier, flex_rank = self.get_summoner_rank(summoner_id)
        #     self.add_player(team_id, summoner_name, champion_name, solo_tier, solo_rank, flex_tier, flex_rank)
        #     print(f"{summoner_name} - {champion_name} - {solo_tier} {solo_rank} - {flex_tier} {flex_rank}")

        self.build()

    def process_player(self, player):
        team_id = player["teamId"]
        summoner_name = player["riotId"]
        summoner_id = player["summonerId"]
        champion_name = get_champion_data_by_champion_id(player["championId"])

        solo_tier, solo_rank, flex_tier, flex_rank = self.get_summoner_rank(summoner_id)
        print(f"{summoner_name} - {champion_name} - {solo_tier} {solo_rank} - {flex_tier} {flex_rank}")

        self.add_player(team_id, summoner_name, champion_name, solo_tier, solo_rank, flex_tier, flex_rank)

    def get_summoner_rank(self, summoner_id):
        url = f"https://vn2.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={API_KEY}"
        data = requests.get(url).json()

        solo_tier = None
        solo_rank = None
        flex_tier = None
        flex_rank = None

        for rank_data in data:
            if rank_data["queueType"] == "RANKED_SOLO_5x5":
                solo_tier = rank_data["tier"]
                solo_rank = rank_data["rank"]
            elif rank_data["queueType"] == "RANKED_FLEX_SR":
                flex_tier = rank_data["tier"]
                flex_rank = rank_data["rank"]

        return solo_tier, solo_rank, flex_tier, flex_rank
    def add_player(self, team_id, summoner_name, champion_name, rank_solo, rank_solo_tier, rank_flex, rank_flex_tier):
        if team_id == 100:
            self.team1.append([summoner_name, champion_name, rank_solo, rank_solo_tier, rank_flex, rank_flex_tier])
        else:
            self.team2.append([summoner_name, champion_name, rank_solo, rank_solo_tier, rank_flex, rank_flex_tier])



    def draw_text(self, text, position, font_size, color):
        font = ImageFont.truetype("../img14.10.1/fonts/Roboto-Regular.ttf", font_size)
        self.draw.text(position, text, color, font=font)


    def draw_champion_icon(self, champion_name, position):
        def load_champion_img(champion_name: str):
            img = Image.open(f"../img14.10.1/champion/tiles/{champion_name}_0.jpg")
            return img
        champion_img = load_champion_img(champion_name)
        # resize to 50x50
        champion_img = champion_img.resize((150, 150))
        self.img.paste(champion_img, position)

    def draw_rank_icon(self, rank, tier, position):
        rank_img = Image.open(f"../img14.10.1/rank_icons/Season_2023_-_{rank.capitalize()}.png")
        rank_img = rank_img.resize((100, 100))
        self.draw_text(tier, (position[0] + 100, position[1] + 50), 30, (255, 255, 255))
        self.img.paste(rank_img, position, rank_img)

    def draw_summoner_info(self, summoner_name:str, champion_name:str, solo_tier:str, solo_rank:str, flex_tier:str, flex_rank:str, team: int, player_index: int):
        x_offset = 0 if team == 1 else 1240

        y_offset = player_index * 200
        self.draw_champion_icon(champion_name, (100 + x_offset, 100+y_offset))
        self.draw_text(summoner_name, (260+x_offset, 100+y_offset), 50, SUMMONER_NAME_COLOR)
        if solo_rank != None:
            self.draw_rank_icon(solo_tier, solo_rank, (260+x_offset, 150+y_offset))
        if flex_rank != None:
            self.draw_rank_icon(flex_tier, flex_rank, (400+x_offset, 150+y_offset))


    def build(self):
        for i, player in enumerate(self.team1):
            self.draw_summoner_info(player[0], player[1], player[2], player[3], player[4], player[5], 1, i)
        for i, player in enumerate(self.team2):
            self.draw_summoner_info(player[0], player[1], player[2], player[3], player[4], player[5], 2, i)
        self.img.save("card.png")


if __name__ == "__main__":
    # get 10 names from the database
    match = MatchData("Căt Đôi nỗi sầu#VN2")
    match.build()
