from collections import Counter
from typing import Hashable

from types1 import Ballot, Result, Scheme
from shared_main import shared_main


def adjust_weights(ballots: list[Ballot], winners, scores, divisor) -> list[Ballot]:
    for ballot in ballots:
        points_to_winners = 0
        for i, candidate in enumerate(ballot.ranking):
            if candidate in winners:
                points_to_winners += scores[i]
        ballot.tally = ballot.tally*(1+points_to_winners/divisor)
    return ballots


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
def borda(intBallots: list[Ballot], numWinners: int) -> Result:
    ballots = floatify_ballots(intBallots)
    curBallots = []
    candidates: set[Hashable] = set()
    for ballot in ballots:
        curBallots.append(ballot)
        for candidate in ballot["ranking"]:
            candidates.add(candidate)
    size = len(candidates)
    if (numWinners >= size):
        return list(candidates)
    points: list[int] = [c for c in range(size - 1, -1, -1)]
    divisor = points[len(points/2)]
    scores: dict[Hashable, float] = {}
    winners = []

    while (len(winners) < numWinners):
        for ballot in ballots:
            for i, candidate in enumerate(ballot["ranking"]):
                scores[candidate] += points[i] * ballot["tally"]
        max_score: int = max(scores.values())
        winner = None
        for candidate in candidates:
            if scores[candidate] == max_score:
                winner = candidate
        candidates.remove(winner)
        winners.append(winner)
        curBallots = adjust_weights(ballots, winners, scores, divisor)

    return winners


scheme: Scheme = borda
name: str = "Borda Count"


def main() -> None:
    shared_main("borda", scheme)


if __name__ == "__main__":
    main()
