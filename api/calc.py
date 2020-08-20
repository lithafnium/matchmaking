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
    for value in team.values():
        # change this to mmr
        db = client.mmr
        # change to key
        col = value
        last_document = op.find_last_document(db, col)
        mmr = float(last_document[0]["mmr"])
        average += mmr
    return average / len(team)


# probability of player a winning the game
def expected_outcome(a, b):
    denom = 1 + math.pow(10, (b - a) / 400)
    return 1 / denom


# finds mmr of a certain player
def find_mmr(player):
    db = client.mmr
    # change to key
    last_document = op.find_last_document(db, player)
    mmr = int(float(last_document[0]["mmr"]))
    return mmr


# stats tracker


def add_team(col, top, jng, mid, adc, sup, game_id):
    db = client.teams
    col = db[col]
    post = {
        "top": top,
        "jng": jng,
        "mid": mid,
        "adc": adc,
        "sup": sup,
        "game_id": game_id,
    }
    col.insert_one(post)
    return post


def update_player_mmr(player, result, own_team_mmr, opp_team_mmr, mu_mmr, game_id):
    # change to mmr
    db = client.mmr
    # change to player
    col = db[player]
    curr_rating = find_mmr(player)

    k_pers = 16
    k_team = 16
    k_mu = 16

    expected_personal = expected_outcome(curr_rating, opp_team_mmr)
    expected_team = expected_outcome(own_team_mmr, opp_team_mmr)
    expected_mu = expected_outcome(curr_rating, mu_mmr)

    updated_rating = (
        curr_rating
        + k_pers * (result - expected_personal)
        + k_team * (result - expected_team)
        + k_mu * (result - expected_mu)
    )
    post = {"mmr": str(updated_rating), "game_id": game_id}
    col.insert_one(post)


# 1 is win, 0 is loss
team1_result = 1
team2_result = 0

# returns an array of mmr rankings
def ladder_ranking():
    # change to mmr
    db = client.mmr
    rankings = {}
    for i in db.list_collection_names():
        # print(int(float(op.find_last_document(db, i)[0]["mmr"])))
        rankings[i] = int(float(op.find_last_document(db, i)[0]["mmr"]))

    rankings_dict = rankings
    sorted_rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)
    print(sorted_rankings)
    return sorted_rankings, rankings_dict


def mmr_history(player):
    db = client.mmr
    col = db[player]
    history = []
    for i in col.find():
        history.append(int(float(i["mmr"])))
    print(history)
    return history


def delete_most_recent_game(player):
    db = client.mmr
    db[player].delete_one(op.find_last_document(client.test, player)[0])


def undo_last_game():
    db = client.mmr
    for i in db.collection_names():
        delete_most_recent_game(i)


def update_all(
    b_top,
    b_jng,
    b_mid,
    b_adc,
    b_sup,
    r_top,
    r_jng,
    r_mid,
    r_adc,
    r_sup,
    one_result,
    two_result,
):
    game_id = get_random_string(20)
    add_team("blue", b_top, b_jng, b_mid, b_adc, b_sup, game_id)
    add_team("red", r_top, r_jng, r_mid, r_adc, r_sup, game_id)
    blue_team = client.teams.blue.find({"game_id": game_id})
    red_team = client.teams.red.find({"game_id": game_id})
    team_one = {
        "top": blue_team[0]["top"],
        "jng": blue_team[0]["jng"],
        "mid": blue_team[0]["mid"],
        "adc": blue_team[0]["adc"],
        "sup": blue_team[0]["sup"],
    }
    team_two = {
        "top": red_team[0]["top"],
        "jng": red_team[0]["jng"],
        "mid": red_team[0]["mid"],
        "adc": red_team[0]["adc"],
        "sup": red_team[0]["sup"],
    }

    team_one_mmr = team_mmr(team_one)
    team_two_mmr = team_mmr(team_two)
    mmr_list = ladder_ranking()[1]
    for key, value in team_one.items():
        mu_mmr = mmr_list[team_two[key]]
        update_player_mmr(
            value, one_result, team_one_mmr, team_two_mmr, mu_mmr, game_id
        )
    for key, value in team_two.items():
        mu_mmr = mmr_list[team_one[key]]
        update_player_mmr(
            value, two_result, team_two_mmr, team_one_mmr, mu_mmr, game_id
        )


# client.test.ian.insert_one(op.post)
# client.test.ian.delete_one(op.find_last_document(client.test, "ian")[0])
# op.add_user("duncan", client.mmr)
# update_all(blue3, red3, 1, 0)
# op.delete_documents_in_all(client.mmr)
# op.add_collections(client.mmr)
# mmr_history("vevey")


def drop_database(db):
    for i in db.list_collection_names():
        db[i].drop()


update_all(
    "aaron",
    "will",
    "vevey",
    "liam",
    "steve",
    "ian",
    "nicky",
    "jocelyn",
    "yuuki",
    "cam",
    0,
    1,
)


#ladder_ranking()

