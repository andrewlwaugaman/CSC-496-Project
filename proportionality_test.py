import argparse
from pprint import pprint
from party_generator import generate_rankings
from stv import stv
from pbv import pbv
from k_borda import k_borda
from haydens_method import process_election
from reweighted_borda import reweighted_borda
from types1 import Scheme
from utility import (
    read_corpus,
    unmarshal_corpus
)


def do_corpus_file(fname: str, scheme: Scheme, winners: int):
    with open(fname, "r") as f:
        data = read_corpus(f)
    corpus = unmarshal_corpus(data)
    elections = corpus.elections
    results = []
    for election in elections:
        results.append(scheme(election.ballots, winners))
    return results
    

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

generate_rankings(args.voters, args.parties, args.party_size, args.max_rankings, max_ranking_length, min_ranking_length, args.elections, args.output)

schemes = [stv, pbv, k_borda, reweighted_borda, process_election]
scheme_names = ["Single Transferable Vote", "Preferential Block Voting", "K-Borda Count", "Reweighted Borda Count", "Hayden's Method"]

for i in range(len(schemes)):
    print(do_corpus_file(args.output, schemes[i], args.winners))