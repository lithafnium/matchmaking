import copy
import random
import mongodboperations as op
import calc as calc
import math
import pymongo
import timeit
from django.utils.crypto import get_random_string

start = timeit.default_timer()

client = pymongo.MongoClient(
    "mongodb+srv://bobjoe:abc@cluster0.j9y1e.mongodb.net/test?retryWrites=true&w=majority"
)



#think if given a big player pool, simulate riots queue matchmaking


def extract_mmr(players):
    mmr_list = []
    for i in players:
        entry = {}
        doc = op.find_last_document(client["rainbow-mmr"], i)
        entry[i] = doc[0]["mmr"]
        mmr_list.append(entry)
    return mmr_list


#MAKE THE ALGORITHM MORE EFFICIENT
def greedy_algo(players):
    players_copy = players.copy()
    random.shuffle(players_copy)
    mmr_list = extract_mmr(players_copy)
    blue_team = []
    red_team = []
    for i in range(4):
        blue_team.append(mmr_list[i])
    for i in range(4):
        red_team.append(mmr_list[4 + i])
    greedy_algo_swap(blue_team, red_team)
    print(blue_team)
    print(avg_mmr(blue_team))
    print(red_team)
    print(avg_mmr(red_team))

def avg_mmr(team):
    avg = 0
    # print(team)
    for i in team:
        # print(list(i.values())[0])
        avg += float(list(i.values())[0])
    return avg / len(team)


def greedy_algo_swap(blue_team, red_team):
    valid_swap = True
    count = 0
    while valid_swap:
        valid_swap = False
        for i in blue_team:
            for j in red_team:
                count += 1
                # print(count)
                # print(valid_swap)
                # print(i)
                # print(j)
                # print(blue_team)
                # print(red_team)
                # print(i)
                # print(j)
                avg_blue = avg_mmr(blue_team)
                avg_red = avg_mmr(red_team)

                blue_copy = copy.deepcopy(blue_team)
                red_copy = copy.deepcopy(red_team)

                blue = i
                red = j
                # print(blue_copy)
                # print("\n")
                # print(red_copy)
                # print("\n")
                # print(i)
                # print("\n")
                # print(j)
                # print("\n")

                blue_team.remove(i)
                red_team.remove(j)
                blue_team.append(red)
                red_team.append(blue)

                diff = abs(avg_mmr(blue_team) - avg_mmr(red_team))

                if diff >= abs(avg_blue - avg_red):
                    blue_team.remove(j)
                    red_team.remove(i)
                    blue_team.append(blue)
                    red_team.append(red)

                    # print(count)
                    # print("START")
                    # print(blue_team)
                    # print("\n")
                    # print(red_team)
                    # print("\n")
                    # print(i)
                    # print("\n")
                    # print(j)
                    # print("\n")
                    # print("AWNRING")
                    continue
                valid_swap = True
                break

    opt_diff = abs(avg_mmr(blue_team) - avg_mmr(red_team))
    # print(count)
    return blue_team, red_team, opt_diff

#deprecated
def greedy_algo_double_swap(blue_team, red_team):
    valid_swap = True
    count = 0
    swapped = False
    while valid_swap:
        blue_swaps = list(get_double_swaps(blue_team))
        red_swaps = list(get_double_swaps(red_team))
        valid_swap = False
        for i in blue_swaps:
            if swapped:
                break
            for j in red_swaps:
                # print(i)
                # print(j)
                # print(blue_team)
                # print(red_team)
                avg_blue = avg_mmr(blue_team)
                avg_red = avg_mmr(red_team)

                blue0 = i[0]
                red0 = j[0]
                blue1 = i[1]
                red1 = j[1]
                # print(blue_copy)
                # print("\n")
                # print(red_copy)
                # print("\n")
                # print(i)
                # print("\n")
                # print(j)
                # print("\n")
                blue_team_copy = copy.deepcopy(blue_team)
                red_team_copy = copy.deepcopy(red_team)

                blue_team_copy.remove(i[0])
                red_team_copy.remove(j[0])
                blue_team_copy.remove(i[1])
                red_team_copy.remove(j[1])
                blue_team_copy.append(red0)
                red_team_copy.append(blue0)
                blue_team_copy.append(red1)
                red_team_copy.append(blue1)

                diff = abs(avg_mmr(blue_team_copy) - avg_mmr(red_team_copy))
                count += 1
                if diff < abs(avg_blue - avg_red):
                    # print(count)
                    # print("START")
                    # print(blue_team)
                    # print("\n")
                    # print(red_team)
                    # print("\n")
                    # print(i)
                    # print("\n")
                    # print(j)
                    # print("\n")
                    print("AWNRING")
                    blue0 = i[0]
                    red0 = j[0]
                    blue1 = i[1]
                    red1 = j[1]

                    blue_team.remove(i[0])
                    red_team.remove(j[0])
                    blue_team.remove(i[1])
                    red_team.remove(j[1])
                    blue_team.append(blue0)
                    red_team.append(red0)
                    blue_team.append(blue1)
                    red_team.append(red1)
                    valid_swap = True
                    swapped = True
                    break

    opt_diff = abs(avg_mmr(blue_team) - avg_mmr(red_team))
    return blue_team, red_team, opt_diff


def get_double_swaps(team):
    for i in range(0, len(team)):
        for j in range(i + 1, len(team)):
            yield [team[i], team[j]]


def brute_force_matchmaking(players):
    player_list = extract_mmr(players)
    team_list = list(acquire_teams(player_list))
    mmr_diff_list = []
    count = 0
    for i in team_list:
        count += 1
        mmr_diff = abs(avg_mmr(player_list) - avg_mmr(i))
        mmr_diff_list.append(mmr_diff)

    index = mmr_diff_list.index(min(mmr_diff_list))

    for i in team_list[index]:
        player_list.remove(i)

    print(team_list[index])
    print(avg_mmr(team_list[index]))
    print(player_list)
    print(avg_mmr(player_list))
    print(count)


def acquire_teams(player_list):
    length = len(player_list)
    count = 0
    # hashcode
    hash_set = set()
    for i in range(0, length):
        for j in range(i + 1, length):
            for k in range(j + 1, length):
                for l in range(k + 1, length):
                    for m in range(l + 1, length):
                        hash_res = sum(hash_custom([9 - i, 9 - j, 9 - k, 9 - l, 9 - m]))
                        hash_set.add(hash_res)
                        hash_check = sum(hash_custom([i, j, k, l, m]))

                        if hash_check not in hash_set:
                            yield [player_list[i], player_list[j], player_list[k], player_list[l], player_list[m]]
                            count += 1


def hash_custom(array):
    array.sort()
    for n in range(5):
        yield array[n] * (10 ** n)


#you can clean this up by abstracting for any number of swaps
def check_single_swaps(blue_team, red_team):
    diff = []
    blue_swap = []
    red_swap = []
    for i in blue_team:
        for j in red_team:
            blue_copy = copy.deepcopy(blue_team)
            red_copy = copy.deepcopy(red_team)

            blue = i
            red = j

            blue_copy.remove(i)
            red_copy.remove(j)
            blue_copy.append(red)
            red_copy.append(blue)

            curr_diff = abs(avg_mmr(blue_copy) - avg_mmr(red_copy))

            diff.append(curr_diff)
            blue_swap.append(i)
            red_swap.append(j)

    index = diff.index(min(diff))

    blue_team[blue_team.index(blue_swap[index])], red_team[red_team.index(red_swap[index])] = \
        red_team[red_team.index(red_swap[index])], blue_team[blue_team.index(blue_swap[index])]


def check_double_swaps(blue_team, red_team):
    blue_swaps = list(get_double_swaps(blue_team))
    red_swaps = list(get_double_swaps(red_team))
    diff = []
    blue_swap = []
    red_swap = []
    for i in blue_swaps:
        for j in red_swaps:
            blue_copy = copy.deepcopy(blue_team)
            red_copy = copy.deepcopy(red_team)

            blue0 = i[0]
            red0 = j[0]
            blue1 = i[1]
            red1 = j[1]

            blue_copy.remove(i[0])
            red_copy.remove(j[0])
            blue_copy.remove(i[1])
            red_copy.remove(j[1])
            blue_copy.append(red0)
            red_copy.append(blue0)
            blue_copy.append(red1)
            red_copy.append(blue1)

            curr_diff = abs(avg_mmr(blue_copy) - avg_mmr(red_copy))
            diff.append(curr_diff)
            blue_swap.append(i)
            red_swap.append(j)

    index = diff.index(min(diff))

    blue_team[blue_team.index(blue_swap[index][0])], red_team[red_team.index(red_swap[index][0])] = \
        red_team[red_team.index(red_swap[index][0])], blue_team[blue_team.index(blue_swap[index][0])]

    blue_team[blue_team.index(blue_swap[index][1])], red_team[red_team.index(red_swap[index][1])] = \
        red_team[red_team.index(red_swap[index][1])], blue_team[blue_team.index(blue_swap[index][1])]


def swapping_algo(players):
    mmr_list = extract_mmr(players)
    blue_team = []
    red_team = []
    for i in range(5):
        blue_team.append(mmr_list[i])
    for i in range(5):
        red_team.append(mmr_list[5 + i])
    blue_copy = copy.deepcopy(blue_team)
    red_copy = copy.deepcopy(red_team)
    check_single_swaps(blue_team, red_team)
    check_double_swaps(blue_copy, red_copy)
    if abs(avg_mmr(blue_team) - avg_mmr(red_team)) > abs(avg_mmr(blue_copy) - avg_mmr(red_copy)):
        print(blue_copy)
        print(avg_mmr(blue_copy))
        print(red_copy)
        print(avg_mmr(red_copy))
    else:
        print(blue_team)
        print(avg_mmr(blue_team))
        print(red_team)
        print(avg_mmr(red_team))



def acquire_teams2(player_list):
    length = len(player_list)
    count = 0
    # hashcode
    hash_set = set()
    for i in range(0, length):
        for j in range(i + 1, length):
            for k in range(j + 1, length):
                for l in range(k + 1, length):
                        hash_res = sum(hash_custom([9 - i, 9 - j, 9 - k, 9 - l]))
                        hash_set.add(hash_res)
                        hash_check = sum(hash_custom([i, j, k, l]))

                        if hash_check not in hash_set:
                            yield [player_list[i], player_list[j], player_list[k], player_list[l]]
                            count += 1


def hash_custom2(array):
    array.sort()
    for n in range(4):
        yield array[n] * (10 ** n)


players = ["nicky", "ian", "colin", "liam", "aaron", "will", "steve", "vevey"]

greedy_algo(players)
# brute_force_matchmaking(players)
# swapping_algo(players)
# print(start)