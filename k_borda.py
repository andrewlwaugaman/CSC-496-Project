from collections import Counter
from typing import Hashable

from types1 import Ballot, Result, Scheme
from shared_main import shared_main


# borda count depends on the size of the ballot,
# so we will use the length of the longest ballot
# (a completely arbitrary choice)
def k_borda(ballots: list[Ballot], numWinners: int) -> Result:

    candidates: set[Hashable] = set()
    for ballot in ballots:
        for candidate in ballot.ranking:
            candidates.add(candidate)
    size = len(candidates)
    if (numWinners >= size):
        return list(candidates)
    points: list[int] = [c for c in range(size - 1, -1, -1)]
    scores: Counter[Hashable] = Counter()

    for ballot in ballots:
        for i, candidate in enumerate(ballot.ranking):
            scores[candidate] += points[i] * ballot.tally
    winner_scores = list(scores.values()).sort(reverse=True)[0:numWinners]
    winners: list[Hashable] = []
    for score in winner_scores:
        to_remove = []
        for candidate in scores.keys():
            if scores[candidate] == score:
                to_remove.append(candidate)
                winners.append(candidate)
        for candidate in to_remove:
            scores.pop(candidate)
    return winners[0:numWinners], scores[winners[numWinners-1]] == scores[winners[numWinners]]


scheme: Scheme = k_borda
name: str = "K Borda Count"


def main() -> None:
    shared_main("k_borda", scheme)


if __name__ == "__main__":
    main()
