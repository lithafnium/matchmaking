import math
import pymongo
import mongodboperations as op
from django.utils.crypto import get_random_string


client = pymongo.MongoClient(
    "mongodb+srv://bobjoe:abc@cluster0.j9y1e.mongodb.net/test?retryWrites=true&w=majority"
)

# red
blue7 = {"top": "aaron", "jng": "will", "mid": "duncan", "adc": "nicky", "sup": "ian"}
red7 = {"top": "dana", "jng": "cam", "mid": "vevey", "adc": "liam", "sup": "steve"}

# blue
blue6 = {"top": "dana", "jng": "cam", "mid": "nicky", "adc": "steve", "sup": "vevey"}
red6 = {"top": "ian", "jng": "liam", "mid": "duncan", "adc": "aaron", "sup": "yuuki"}

# blue
blue5 = {"top": "nicky", "jng": "aaron", "mid": "yuuki", "adc": "liam", "sup": "dana"}
red5 = {"top": "cam", "jng": "vevey", "mid": "steve", "adc": "duncan", "sup": "ian"}

# red
blue4 = {"top": "cam", "jng": "steve", "mid": "aaron", "adc": "will", "sup": "ian"}
red4 = {"top": "nicky", "jng": "liam", "mid": "yuuki", "adc": "vevey", "sup": "jocelyn"}

# blue
blue3 = {"top": "vevey", "jng": "aaron", "mid": "steve", "adc": "liam", "sup": "ian"}
red3 = {"top": "shane", "jng": "will", "mid": "yuuki", "adc": "nicky", "sup": "cam"}

# blue
blue2 = {"top": "vevey", "jng": "yuuki", "mid": "erik", "adc": "liam", "sup": "cam"}
red2 = {"top": "will", "jng": "nicky", "mid": "aaron", "adc": "steve", "sup": "ian"}

# red
blue1 = {"top": "aaron", "jng": "vevey", "mid": "cam", "adc": "liam", "sup": "steve"}
red1 = {"top": "will", "jng": "erik", "mid": "ian", "adc": "nicky", "sup": "yuuki"}

# finds average team mmr
def team_mmr(team):
    average = 0
    for key in team.keys():
        # change this to mmr
        db = client["rainbow-mmr"]
        # change to key
        col = key
        if key == "_id" or key == "game_id" or key == "rounds_won":
            continue
        last_document = op.find_last_document(db, col)
        mmr = float(last_document[0]["mmr"])
        average += mmr
    return average / (len(team)-3)


# probability of player a winning the game
def expected_outcome(a, b):
    denom = 1 + math.pow(10, (b - a) / 400)
    return 1 / denom


# finds mmr of a certain player
def find_mmr(player):
    db = client["rainbow-mmr"]
    # change to key
    last_document = op.find_last_document(db, player)
    mmr = int(float(last_document[0]["mmr"]))
    return mmr


# stats tracker

##SC
def add_team(col, team, rounds, game_id):
    db = client["rainbow-teams"]
    col = db[col]
    post = {
    }
    for x in team:
        post[x["name"]] = x
    
    post["rounds_won"] = rounds
    post["game_id"] = game_id
    col.insert_one(post)
    return post

#MAKE THIS SCALABLE
def update_player_mmr(player, result, own_team_mmr, opp_team_mmr, KAT, round_diff, game_id):
    # change to mmr
    db = client["rainbow-mmr"]
    # change to player
    col = db[player]
    curr_rating = find_mmr(player)

    k_pers = 26
    k_team = 12
    ##stats, kills, assist, points
    ##KAT is kills, assists while also paired with team size



    expected_personal = expected_outcome(curr_rating, opp_team_mmr)
    expected_team = expected_outcome(own_team_mmr, opp_team_mmr)


    win_bonus = 0
    if result == 1:
        win_bonus = 2

    updated_rating = (
        + (k_pers * (result - expected_personal)
        + k_team * (result - expected_team)
        + KAT * 2 * (1-expected_personal)**2
        + win_bonus
        + 1.5 * round_diff)
    )

    if result == 0:
        updated_rating *= 1.6

    updated_rating += curr_rating
    

    # if player == "aaron":
    #     print(player)
    #     print(expected_personal)
    #     print(k_pers * (result - expected_personal))
    #     print(k_team * (result - expected_team))
    #     print(KAT * 2 * (1-expected_personal))
    #     print(result - expected_personal)
    #     print((k_pers * (result - expected_personal)
    #     + k_team * (result - expected_team)
    #     + KAT * 2 * (1-expected_personal)**2
    #     + win_bonus
    #     + 1.5 * round_diff))

    post = {"mmr": str(updated_rating), "game_id": game_id}
    col.insert_one(post)


# 1 is win, 0 is loss
team1_result = 1
team2_result = 0

# returns an array of mmr rankings
def ladder_ranking():
    # change to mmr
    db = client["rainbow-mmr"]
    rankings = {}
    for i in db.list_collection_names():
        # print(int(float(op.find_last_document(db, i)[0]["mmr"])))
        rankings[i] = int(float(op.find_last_document(db, i)[0]["mmr"]))

    rankings_dict = rankings
    sorted_rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
    print(sorted_rankings)
    return sorted_rankings, rankings_dict


def mmr_history(player):
    db = client["rainbow-mmr"]
    col = db[player]
    history = []
    for i in col.find():
        history.append(int(float(i["mmr"])))
    print(history)
    return history


def delete_most_recent_game(player):
    db = client["rainbow-mmr"]
    db[player].delete_one(op.find_last_document(client["rainbow-mmr"], player)[0])


def undo_last_game():
    db = client["rainbow-teams"]
    blue_team = op.find_last_document(db, "blue")[0]
    orange_team = op.find_last_document(db, "orange")[0]
    for key in blue_team.keys():
        if key == "_id" or key == "game_id" or key == "rounds_won":
            continue
        delete_most_recent_game(key)
    for key in orange_team.keys():
        if key == "_id" or key == "game_id" or key == "rounds_won":
            continue
        delete_most_recent_game(key)
    db["blue"].delete_one(op.find_last_document(db, "blue")[0])
    db["orange"].delete_one(op.find_last_document(db, "orange")[0])

#abstraction

def update_all():  #b_team, o_team, blue_result, orange_result, b_rounds, o_rounds

    b_input = input("Input blue team separated by a space in the format name/kills/assists: ")
    b_names = [x.split("/")[0] for x in b_input.split()]
    b_team = [{"name": x.split("/")[0], "kills": int(x.split("/")[1]), "assists": int(x.split("/")[2])} for x in b_input.split()]
    # print(b_team)
    o_input = input("Input orange team separated by a space in the format name/kills/assists: ")
    
    o_names = [x.split("/")[0] for x in o_input.split()]
    o_team = [{"name": x.split("/")[0], "kills": int(x.split("/")[1]), "assists": int(x.split("/")[2])} for x in o_input.split()]
    # print(o_team)

    result_input = input("Input blue result/orange result and blue rounds won/orange rounds won separated by a space: ")
    blue_result = int(result_input.split()[0].split("/")[0])
    orange_result = int(result_input.split()[0].split("/")[1])
    b_rounds = int(result_input.split()[1].split("/")[0])
    o_rounds = int(result_input.split()[1].split("/")[1])
    print(b_rounds)
    print(o_rounds)

    for b in b_names:
        if (not (b in client["rainbow-mmr"].list_collection_names())):
            op.add_user(b, client["rainbow-mmr"])

    for o in o_names:
        if (not (o in client["rainbow-mmr"].list_collection_names())):
            op.add_user(o, client["rainbow-mmr"])


    game_id = get_random_string(20)
    add_team("blue", b_team, b_rounds, game_id) #######IF YOU WANT TO ADD MORE TO ADD TEAMS, YOU HAVE TO CHECK IF ITS A NAME
    add_team("orange", o_team, o_rounds, game_id)
    blue_team = client["rainbow-teams"].blue.find({"game_id": game_id})
    orange_team = client["rainbow-teams"].orange.find({"game_id": game_id})

    
    team_one_mmr = team_mmr(blue_team[0])
    team_two_mmr = team_mmr(orange_team[0])
    mmr_list = ladder_ranking()[1]
    # print(team_one_mmr)
    # print(team_two_mmr)

    b_len = len(blue_team[0])
    o_len = len(orange_team[0])
    for key, value in blue_team[0].items():
        if (key == "_id" or key == "game_id" or key == "rounds_won"):
            continue
        kat = (value["kills"] + value["assists"] * 0.5) / (5 / b_len)
        kat = kat * (1 + (b_rounds + o_rounds)/10)
        update_player_mmr(
            value["name"], blue_result, team_one_mmr, team_two_mmr, kat, b_rounds - o_rounds, game_id
        )
    for key, value in orange_team[0].items():
        if (key == "_id" or key == "game_id" or key == "rounds_won"):
            continue
        kat = (value["kills"] + value["assists"] * 0.5) / (5 / o_len)
        kat = kat * (1 + (b_rounds + o_rounds)/10)
        update_player_mmr(
            value["name"], orange_result, team_two_mmr, team_one_mmr, kat, o_rounds - b_rounds, game_id
        )


# client.test.ian.insert_one(op.post)
# client.test.ian.delete_one(op.find_last_document(client.test, "ian")[0])

# update_all(blue3, red3, 1, 0)
#op.delete_documents_in_all(client.mmr)
#op.add_collections(client.mmr)
# mmr_history("vevey")



def drop_database(db):
    for i in db.list_collection_names():
        db[i].drop()



##TEST GAME
nicky = {"name": "nicky", "kills": 4, "assists": 3}
will = {"name": "will", "kills": 5, "assists": 7}
steve = {"name": "steve", "kills": 2, "assists": 1}
liam = {"name": "liam", "kills": 1, "assists": 3}

vevey = {"name": "vevey", "kills": 15, "assists": 3}
colin = {"name": "colin", "kills": 8, "assists": 0}
aaron = {"name": "aaron", "kills": 0, "assists": 3}
ian = {"name": "ian", "kills": 11, "assists": 7}

rain_blue = [nicky, will, steve, liam]
rain_orange = [vevey, colin, aaron, ian]



#update_all(rain_blue, rain_orange, 0, 1, 1, 3)
#firstgame

nicky1 = {"name": "nicky", "kills": 7, "assists": 1}
will1 = {"name": "will", "kills": 7, "assists": 0}
vevey1 = {"name": "vevey", "kills": 6, "assists": 1}
colin1 = {"name": "colin", "kills": 0, "assists": 1}

ian1 = {"name": "ian", "kills": 6, "assists": 3}
aaron1 = {"name": "aaron", "kills": 8, "assists": 0}
riley1 = {"name": "riley", "kills": 4, "assists": 0}
liam1 = {"name": "liam", "kills": 4, "assists": 1}

rain_blue1 = [nicky1, will1, vevey1, colin1]
rain_orange1 = [ian1, aaron1, riley1, liam1]

#second game


steve2 = {"name": "steve", "kills": 7, "assists": 4}
aaron2 = {"name": "aaron", "kills": 7, "assists": 1}
will2 = {"name": "will", "kills": 6, "assists": 3}
nicky2 = {"name": "nicky", "kills": 5, "assists": 3}

vevey2 = {"name": "vevey", "kills": 6, "assists": 2}
colin2 = {"name": "colin", "kills": 7, "assists": 1}
ian2 = {"name": "ian", "kills": 4, "assists": 1}
liam2 = {"name": "liam", "kills": 2, "assists": 1}

rain_blue2 = [nicky2, will2, steve2, aaron2]
rain_orange2 = [ian2, colin2, vevey2, liam2]




#third game

ian3 = {"name": "ian", "kills": 7, "assists": 4}
vevey3 = {"name": "vevey", "kills": 5, "assists": 1}
aaron3 = {"name": "aaron", "kills": 0, "assists": 3}
liam3 = {"name": "liam", "kills": 7, "assists": 0}

steve3 = {"name": "steve", "kills": 1, "assists": 0}
will3 = {"name": "will", "kills": 2, "assists": 1}
nicky3 = {"name": "nicky", "kills": 3, "assists": 0}
colin3 = {"name": "colin", "kills": 2, "assists": 1}

rain_blue3 = [ian3, vevey3, aaron3, liam3]
rain_orange3 = [steve3, will3, nicky3, colin3]






#fourth game

ian4 = {"name": "ian", "kills": 2, "assists": 1}
vevey4 = {"name": "vevey", "kills": 4, "assists": 1}
steve4 = {"name": "steve", "kills": 3, "assists": 1}
nicky4 = {"name": "nicky", "kills": 7, "assists": 0}

aaron4 = {"name": "aaron", "kills": 1, "assists": 0}
will4 = {"name": "will", "kills": 5, "assists": 1}
liam4 = {"name": "liam", "kills": 3, "assists": 0}
colin4 = {"name": "colin", "kills": 1, "assists": 1}

rain_blue4 = [ian4, vevey4, steve4, nicky4]
rain_orange4 = [aaron4, will4, liam4, colin4]



# op.add_user("vevey", client["rainbow-mmr"])
# op.add_user("will", client["rainbow-mmr"])
# op.add_user("ian", client["rainbow-mmr"])
# op.add_user("nicky", client["rainbow-mmr"])
# op.add_user("aaron", client["rainbow-mmr"])
# op.add_user("liam", client["rainbow-mmr"])
# op.add_user("colin", client["rainbow-mmr"])
# op.add_user("steve", client["rainbow-mmr"])
# op.add_user("riley", client["rainbow-mmr"])

# update_all(rain_blue1, rain_orange1, 0, 1, 3, 4)
# update_all(rain_blue2, rain_orange2, 1, 0, 5, 3)
# update_all(rain_blue3, rain_orange3, 1, 0, 4, 0)
# update_all(rain_blue4, rain_orange4, 1, 0, 4, 1)

# drop_database(client["rainbow-mmr"])
# drop_database(client["rainbow-teams"])

#undo_last_game()
###ROUND DIFFERENCE
update_all()



ladder_ranking()

