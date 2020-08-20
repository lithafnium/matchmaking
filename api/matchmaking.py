import mongodboperations as op
import calc
import math
import pymongo
from django.utils.crypto import get_random_string

client = pymongo.MongoClient(
    "mongodb+srv://bobjoe:abc@cluster0.j9y1e.mongodb.net/test?retryWrites=true&w=majority"
)

players = ["vevey", "ian", "cam", "nicky", "steve", "liam", "aaron", "will", "yuuki", "erik"]

def extract_mmr(players):
  mmr_list = {}
  for i in players:
    mmr_list[i] = client.mmr[i]
  return mmr_list

def brute_matchmaking(players):
  mmr_list = extract_mmr(players)
  return min(permute_teams(mmr_list))

def permute_teams(mmr_list):
  
  return 