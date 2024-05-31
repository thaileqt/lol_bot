from src.utils import extract_name_tag
from src.fetch_data import get_lol_data, get_match_data, get_champion_data_by_champion_id
import threading
import os
import requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('API_KEY')


def process_rank_data(name_with_tag: str):
   """
   Processes League of Legends data (list of dictionaries) and returns a formatted string.


   Args:
     data: List of dictionaries containing league data for a user.


   Returns:
     A string containing formatted information about the user's rank and win/loss rates.
   """
   player_name, tag = extract_name_tag(name_with_tag)
   if not player_name or not tag:
       return "Player not found!"
   data = get_lol_data(name_with_tag)
   if not data:
       return "Player not found!"
   result = ""


   result += f"Player: {name_with_tag}\n"




   for entry in data:
       if entry["queueType"] == "CHERRY":
           continue
       queue_type = entry["queueType"].replace("RANKED_", "")
       win_rate = round((entry["wins"] / (entry["wins"] + entry["losses"])) * 100, 2)


       # Use f-strings for clear and concise string formatting
       result += f"Rank {queue_type}: **{entry['tier']} {entry['rank']}** - W/L: {entry['wins']}/{entry['losses']} - WR: {win_rate}%\n"


   return result



if __name__ == "__main__":
   pass