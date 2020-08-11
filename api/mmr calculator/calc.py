import math
import pymongo
import mongodboperations as op

client = pymongo.MongoClient("mongodb+srv://bobjoe:abc@cluster0.j9y1e.mongodb.net/test?retryWrites=true&w=majority")

team1 = {
    "vevey": "top",
    "yuuki": "jng",
    "erik": "mid",
    "liam": "adc",
    "cam": "sup"
}
team2 = {
    "will": "top",
    "nicky": "jng",
    "aaron": "mid",
    "steve": "adc",
    "ian": "sup"
}

team1G1 = {
    "aaron": "top",
    "vevey": "jng",
    "cam": "mid",
    "liam": "adc",
    "steve": "sup"
}
team2G1 = {
    "will": "top",
    "erik": "jng",
    "ian": "mid",
    "nicky": "adc",
    "yuuki": "sup"
}


def team_mmr(team):
    average = 0
    for key in team.keys():
        # change this to mmr
        db = client.mmr
        # change to key
        col = key
        last_document = op.find_last_document(db, col)
        mmr = int(float(last_document[0]["mmr"]))
        average += mmr
    return average / len(team)


# probability of player a winning the game
def expected_outcome(a, b):
    denom = 1 + math.pow(10, (b - a) / 400)
    return 1 / denom


#stats tracker


def update_player_mmr(player, result, own_team, opp_team):
    # change to mmr
    db = client.mmr
    # change to player
    col = db[player]
    curr_rating = int(float(op.find_last_document(db, player)[0]["mmr"]))
    # k-factor of 24, taken from elo wiki
    k_pers = 16
    k_team = 16
    k_mu = 16

    expected_personal = expected_outcome(curr_rating, team_mmr(opp_team))
    expected_team = expected_outcome(team_mmr(own_team), team_mmr(opp_team))

    opp_rating = int(float(op.find_last_document(db, player)[0]["mmr"]))
    expected_mu = expected_outcome(curr_rating, opp_rating)

    updated_rating = curr_rating + k_pers*(result - expected_personal) + k_team*(result - expected_team) \
                     + k_mu*(result - expected_mu)
    post = {"mmr": str(updated_rating)}
    col.insert_one(post)

# 1 is win, 0 is loss
team1_result = 1
team2_result = 0


def update_all(team_one, team_two, one_result, two_result):
    for key in team_one.keys():
        update_player_mmr(key, one_result, team_one, team_two)
    for key in team_two.keys():
        update_player_mmr(key, two_result, team_two, team_one)


def ladder_ranking():
    # change to mmr
    db = client.mmr
    rankings = {}
    for i in db.list_collection_names():
        #print(int(float(op.find_last_document(db, i)[0]["mmr"])))
        rankings[i] = (int(float(op.find_last_document(db, i)[0]["mmr"])))

    sorted_rankings = sorted(rankings.items(), key=lambda x: x[1], reverse=True)

    print(sorted_rankings)


update_all(team1, team2, 1, 0)

ladder_ranking()