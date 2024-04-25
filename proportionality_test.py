import argparse
from pprint import pprint
from party_generator import generate_rankings
from stv import stv
from pbv import pbv
from k_borda import k_borda
from haydens_method import process_election
from reweighted_borda import reweighted_borda
from types1 import Scheme
    

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

elections = generate_rankings(args.voters, args.parties, args.party_size, args.max_rankings, max_ranking_length, min_ranking_length, args.elections, args.output)

schemes = [stv, pbv, k_borda, reweighted_borda, process_election]
scheme_names = ["Single Transferable Vote", "Preferential Block Voting", "K-Borda Count", "Reweighted Borda Count", "Hayden's Method"]
party_names = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"][0:args.parties]
num_winners = int(args.winners)

total_disproportionalities = {}
for scheme in scheme_names:
    total_disproportionalities[scheme] = 0

print()
for election in elections:
    #for ballot in election.ballots:
    #    print(ballot)
    for i in range(len(schemes)):
        winners = schemes[i](election.ballots, num_winners)
        election.winners[scheme_names[i]] = winners
        disproportionality = 0
        party_winners = {}
        for party in party_names:
            party_winners[party] = 0
        for winner in winners:
            party_winners[winner[0]] += 1
        for party in party_names:
            disproportionality += pow((party_winners[party]/num_winners)-(election.first_place_counts[party]/args.voters), 2)/(election.first_place_counts[party]/args.voters)
        election.disproportionality[scheme_names[i]] = disproportionality
        total_disproportionalities[scheme_names[i]] += disproportionality


for i, election in enumerate(elections):
    print("\nElection " + str(i+1) + " results:\n")
    for scheme in scheme_names:
        print(scheme + " winners (ordered): " + str(election.winners[scheme]))
        print(scheme + " winners (sorted): " + str(sorted(election.winners[scheme])))
        print(scheme + " disproportionality: " + str(election.disproportionality[scheme]))
        print()

print()
for scheme in scheme_names:
    print("Average disproportionality of " + scheme + ": " + str(total_disproportionalities[scheme]/args.elections))

print()