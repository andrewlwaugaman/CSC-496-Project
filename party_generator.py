import argparse
import itertools
import random
import json
import sys

from types1 import Election, Ballot

parser = argparse.ArgumentParser()
parser.add_argument("--num-voters", dest="voters", default=10000, type=int)
parser.add_argument("--num-parties", dest="parties", default=4, type=int)
parser.add_argument("--party-size", dest="party_size", default=3, type=int)
parser.add_argument("--max-unique-rankings", dest="max_rankings", default=30, type=int)
parser.add_argument(
    "--max-ranking-length", dest="max_ranking_length", default=-1, type=int
)
parser.add_argument(
    "--min-ranking-length", dest="min_ranking_length", default=-1, type=int
)
parser.add_argument("--num-elections", dest="elections", default=1, type=int)
parser.add_argument("--output-file", dest="output", default="electionCorpus.json")

# Unused, just here so running the other doesn't break it
parser.add_argument("--num-winners", dest="winners", default=6)

args = parser.parse_args()

#random.seed(1)

max_ranking_length = 0
min_ranking_length = 0

if args.party_size > 26:
    party_size = 26
elif args.party_size < 1:
    party_size = 1
else:
    party_size = args.party_size
if args.max_ranking_length == -1:
    max_ranking_length = args.parties*party_size
else:
    max_ranking_length = args.max_ranking_length
if args.min_ranking_length == -1:
    min_ranking_length = max_ranking_length
else:
    min_ranking_length = min(args.min_ranking_length, max_ranking_length)

def generate_rankings(votes, parties, party_size, unique_rankings, max_ranking_length, min_ranking_length, num_elections, output_file):
    elections = []
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    possible_party_rankings = []
    unaffiliated_rankings = (list(itertools.permutations(range(0, party_size), party_size)))
    for i in range(parties):
        party_ranking_group = []
        for ranking in unaffiliated_rankings:
            possible_ranking = []
            for candidate in ranking:
                possible_ranking.append(alphabet[i] + "." + str(candidate))
            party_ranking_group.append(possible_ranking)
        possible_party_rankings.append(party_ranking_group)

    possible_party_ranking_permutations = list(itertools.permutations(possible_party_rankings, parties))
    possible_rankings_max_length = []
    for i in possible_party_ranking_permutations:
        possible_rankings_max_length.extend(list(itertools.product(*i)))
    possible_rankings_max_length_untupled: list[list[int]] = []
    for i in possible_rankings_max_length:
        untupled = []
        for j in i:
            for k in j:
                untupled.append(k)
        possible_rankings_max_length_untupled.append(untupled)

    possible_rankings = set()
    for i in range(min_ranking_length, max_ranking_length + 1):
        for j in possible_rankings_max_length_untupled:
            possible_rankings.add(tuple(j[0:i]))

    max_rankings = unique_rankings
    if max_rankings == -1:
        max_rankings = len(possible_rankings)

    for i in range(num_elections):
        rankings = set()
        for _ in range(max_rankings):
            if len(possible_rankings) > 0:
                rankings.add(possible_rankings.pop())
        vote_partitions = []
        for _ in range(len(rankings) - 1):
            vote_partitions.append(random.randrange(0, votes))
        vote_partitions.append(0)
        vote_partitions.append(votes)
        vote_partitions.sort()
        rankings = list(rankings)
        elections.append({"ballots": []})
        for j in range(1, len(vote_partitions)):
            if (vote_partitions[j] - vote_partitions[j - 1] != 0):
                elections[i]["ballots"].append(
                    {
                        "ranking": rankings[j - 1],
                        "count": vote_partitions[j] - vote_partitions[j - 1],
                    }
                )
        elections[i]["first_place_counts"] = {}
        for j in range(parties):
            elections[i]["first_place_counts"][alphabet[j]] = 0
        for ballot in elections[i]["ballots"]:
            elections[i]["first_place_counts"][ballot["ranking"][0][0]] += ballot["count"]
        #print(elections[i])
        for ranking in rankings:
            possible_rankings.add(ranking)

    return_dict = {
        "num_voters": args.voters,
        "num_candidates": args.parties*party_size,
        "max_unique_rankings": max_rankings,
        "max_ranking_length": max_ranking_length,
        "min_ranking_length": min_ranking_length,
        "num_elections": args.elections,
        "elections": elections,
    }

    if len(output_file) == 0:
        json.dump(return_dict, sys.stdout, indent=4)
    else:
        with open(output_file, "w") as outfile:
            json.dump(return_dict, outfile, indent=4)
    
    altElections: list[Election] = []
    for election in elections:
        altBallots = []
        for ballot in election["ballots"]:
            altBallots.append(Ballot(tuple(ballot["ranking"]), ballot["count"]))
        altElections.append(Election(altBallots, {}, election["first_place_counts"], {}))

    return altElections

generate_rankings(args.voters, args.parties, args.party_size, args.max_rankings, max_ranking_length, min_ranking_length, args.elections, args.output)