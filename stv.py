from collections import Counter
from typing import Hashable

from types1 import Ballot, Result, Scheme
from shared_main import shared_main

def floatify_ballots(ballots: list[Ballot]):
    floatedBallots = []
    for ballot in ballots:
        floatedBallots.append({
            "tally": float(ballot.tally),
            "ranking": list(ballot.ranking)
        })
    return floatedBallots

def count_votes(ballots, candidates: dict[Hashable, float]) -> dict[Hashable, float]:
    counts = {}
    for candidate in candidates.keys():
        counts[candidate] = 0.0
    for ballot in ballots:
        multiplier = 1.0
        for candidate in ballot["ranking"]:
            counts[candidate] += ballot["tally"] * (multiplier * candidates[candidate])
            multiplier *= (1-candidates[candidate])
    return counts

def calculate_quota(ballots, numWinners, candidates):
    quota = 0.0
    for ballot in ballots:
        quota += ballot["tally"]
        no_hopeful = True
        for candidate in ballot["ranking"]:
            if candidates[candidate] == 1:
                no_hopeful = False
        if no_hopeful:
            excess = ballot["tally"]
            for candidate in ballot["ranking"]:
                excess *= (1-candidates[candidate])
            quota -= excess
    quota = quota/(numWinners+1)
    return quota

def recalculate_weights(candidates: dict[Hashable, float], quota, counts):
    for candidate in candidates.keys():
        if (candidates[candidate] != 1 and candidates[candidate] != 0) or (candidates[candidate] == 1 and counts[candidate] > quota):
            candidates[candidate] = candidates[candidate] * quota/counts[candidate]
    return candidates

def stv(intBallots: list[Ballot], numWinners: int) -> Result:
    # A value of 0 implies a candidate is eliminated, a value of 1 implies a candidate is hopeful,
    # and a value between 0 and 1 implies the candidate has been elected.
    candidates: dict[Hashable, float] = {}
    ballots = floatify_ballots(intBallots)
    for ballot in ballots:
        for candidate in ballot["ranking"]:
            candidates[candidate] = 1
    if (numWinners >= len(candidates)):
        return list(candidates.keys())
    
    winners = set()
    while (len(winners) < numWinners):
        quota = calculate_quota(ballots, numWinners, candidates)
        counts = count_votes(ballots, candidates)
        winner_added = False
        for candidate in counts.keys():
            if counts[candidate] >= quota:
                winners.add(candidate)
                winner_added = True
        if winner_added == False:
            quota_adjustment_needed = False
            for candidate in winners:
                if 0.9999 < counts[candidate] / quota < 1.0001:
                    quota_adjustment_needed = True
            if quota_adjustment_needed == False:
                min_vote = min(counts.values())
                loser = None
                for candidate in candidates.keys():
                    if counts[candidate] == min_vote:
                        loser = candidate
                candidates[loser] = 0
        candidates = recalculate_weights(candidates, quota, counts)
        print("A")
    return list(winners)


scheme: Scheme = stv
name: str = "Single Transferrable Vote"


def main() -> None:
    shared_main("stv", scheme)


if __name__ == "__main__":
    main()
