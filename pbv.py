from collections import Counter
from typing import Hashable

from types1 import Ballot, Result, Scheme
from shared_main import shared_main

def eliminate_candidate(ballots: list[Ballot], candidate: Hashable) -> list[Ballot]:
    newBallots: list[tuple[Hashable]] = []
    for ballot in ballots:
        newRanking = list(ballot.ranking)
        if (candidate in newRanking):
            newRanking.remove(candidate)
        if len(newRanking) > 0:
            newBallot = Ballot(ranking=newRanking, tally=ballot.tally)
            newBallots.append(newBallot)
    return newBallots


def count_first(ballots: list[Ballot]) -> dict[Hashable, int]:
    firstCounts = {}
    for ballot in ballots:
        for candidate in ballot.ranking:
            firstCounts[candidate] = 0
    for ballot in ballots:
        if len(ballot.ranking) > 0:
            firstCounts[ballot.ranking[0]] += ballot.tally
    return firstCounts


def pbv(ballots: list[Ballot], numWinners: int) -> Result:
    winners: list[Hashable] = []
    candidates = set()
    for ballot in ballots:
        for candidate in ballot.ranking:
            candidates.add(candidate)
    if (numWinners >= len(candidates)):
        return list(candidates)
    tie = False
    while len(winners < numWinners):
        temp_ballots = []
        for ballot in ballots:
            temp_ballots.append(ballot)
        temp_candidates = set()
        for candidate in candidates:
            temp_candidates.add(candidate)
        while len(temp_candidates) > 1 and not tie:
            firstCounts = count_first(temp_ballots)
            firstCountsList = list(firstCounts.values())
            losers = set()
            lowest = min(firstCountsList)
            highest = max(firstCountsList)
            if (highest >= ((sum(firstCountsList)+1)/2)):
                for candidate in temp_candidates:
                    if firstCounts[candidate] == highest:
                        return candidate, True
            if (lowest != max(firstCountsList)):
                for candidate in temp_candidates:
                    if firstCounts[candidate] == lowest:
                        losers.add(candidate)
                if (len(losers) > 1):
                    winners = list(candidates)
                    return winners[0], False
                loser = losers.pop()
                temp_ballots = eliminate_candidate(ballots, loser)
                temp_candidates.remove(loser)
            else:
                tie = True
        winner = temp_candidates.pop()
        winners.append(winner)
        candidates.remove(winner)
        ballots = eliminate_candidate(ballots, winner)
    return winners[0], len(winners) == 1


scheme: Scheme = pbv
name: str = "Preferential Block Voting"


def main() -> None:
    shared_main("pbv", scheme)


if __name__ == "__main__":
    main()
