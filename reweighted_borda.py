from collections import Counter
import copy
from typing import Hashable

from types1 import Ballot, Result, Scheme
from shared_main import shared_main

#https://electowiki.org/wiki/Reweighted_range_voting

def adjust_weights(ballots: list[Ballot], winners, points, divisor) -> list[Ballot]:
    newBallots = copy.deepcopy(ballots)
    for ballot in newBallots:
        points_to_winners = 0
        for i, candidate in enumerate(ballot["ranking"]):
            if candidate in winners:
                points_to_winners += points[i]
        ballot["tally"] = ballot["tally"]/(1+points_to_winners/divisor)
    return newBallots


def floatify_ballots(ballots: list[Ballot]):
    floatedBallots = []
    for ballot in ballots:
        floatedBallots.append({
            "tally": float(ballot.tally),
            "ranking": ballot.ranking
        })
    return floatedBallots


# borda count depends on the size of the ballot,
# so we will use the length of the longest ballot
# (a completely arbitrary choice)
def reweighted_borda(intBallots: list[Ballot], numWinners: int) -> Result:
    ballots = floatify_ballots(intBallots)
    curBallots = []
    candidates: set[Hashable] = set()
    scores: dict[Hashable, float] = {}
    for ballot in ballots:
        curBallots.append(ballot)
        for candidate in ballot["ranking"]:
            candidates.add(candidate)
            scores[candidate] = 0
    size = len(candidates)
    if (numWinners >= size):
        return list(candidates)
    points: list[int] = [c for c in range(size - 1, -1, -1)]
    divisor = points[0]
    winners = []
    #print(ballots)

    while (len(winners) < numWinners):
        for ballot in curBallots:
            for i, candidate in enumerate(ballot["ranking"]):
                scores[candidate] += points[i] * ballot["tally"]
        winner = None
        max_score = 0.0
        for candidate in candidates:
            if scores[candidate] > max_score and candidate not in winners:
                max_score = scores[candidate]
                winner = candidate
        winners.append(winner)
        curBallots = adjust_weights(ballots, winners, points, divisor)
        #print(curBallots)
        for candidate in candidates:
            scores[candidate] = 0

    return winners


scheme: Scheme = reweighted_borda
name: str = "Reweighted Borda"


def main() -> None:
    shared_main("reweighted_borda", scheme)


if __name__ == "__main__":
    main()
