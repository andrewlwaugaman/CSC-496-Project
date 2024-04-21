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

def count_first(ballots) -> dict[Hashable, float]:
    firstCounts = {}
    for ballot in ballots:
        for candidate in ballot["ranking"]:
            firstCounts[candidate] = 0.0
    for ballot in ballots:
        if len(ballot["ranking"]) > 0:
            firstCounts[ballot["ranking"][0]] += ballot["tally"]
    return firstCounts

def calculate_quota(ballots, numWinners):
    quota = 0.0
    for ballot in ballots:
        quota += ballot["tally"]
    quota = quota/(numWinners+1)
    quotaInt = int(quota) + 1
    return quotaInt

def transfer_votes(ballots, winners, quota):
    for winner in winners:
        transferableVotes = 0
        totalVotes = 0
        for ballot in ballots:
            if ballot["ranking"][0] == winner:
                while len(ballot["ranking"]) > 0 and ballot["ranking"][0] in winners:
                    ballot["ranking"] = ballot["ranking"][1:]
                if len(ballot["ranking"]) == 0:
                    totalVotes += ballot["tally"]
                else:
                    transferableVotes += ballot["tally"]
        totalVotes += transferableVotes
        for ballot in ballots:
            if len(ballot["ranking"]) != 0:
                ballot["tally"] = (ballot["tally"]/transferableVotes)*(totalVotes-quota)
    return ballots

def eliminate_candidate(ballots, candidate: Hashable) -> list[Ballot]:
    newBallots: list[tuple[Hashable]] = []
    for ballot in ballots:
        newRanking = list(ballot["ranking"])
        if (candidate in newRanking):
            if len(newRanking) > 1:
                newRanking.remove(candidate)
                newBallot = {"ranking": newRanking, "tally": ballot["tally"]}
                newBallots.append(newBallot)
    return newBallots

def stv(intBallots: list[Ballot], numWinners: int) -> Result:
    candidates: set[Hashable] = set()
    ballots = floatify_ballots(intBallots)
    for ballot in ballots:
        for candidate in ballot["ranking"]:
            candidates.add(candidate)
    if (numWinners >= len(candidates)):
        return list(candidates)
    
    winners = set()
    quota = calculate_quota(ballots, numWinners)
    while (len(winners) < numWinners):
        firstCounts = count_first(ballots)
        winnersAdded = False
        for candidate in candidates:
            if firstCounts[candidate] > quota:
                winners.add(candidate)
                winnersAdded = True
        for winner in winners:
            if winner in candidates:
                candidates.remove(winner)
        if len(winners) < numWinners:
            if winnersAdded:
                ballots = transfer_votes(ballots, winners, quota)
            else:
                loserCount = min(firstCounts.values())
                eliminated = False
                loser = ""
                for candidate in candidates:
                    if firstCounts[candidate] == loserCount and not eliminated:
                        loser = candidate
                        eliminated = True
                ballots = eliminate_candidate(ballots, loser)
                candidates.remove(loser)
                if (len(winners) + len(candidates) == numWinners):
                    for candidate in candidates:
                        winners.add(candidate)
                    return winners
    return winners


scheme: Scheme = stv
name: str = "Single Transferrable Vote"


def main() -> None:
    shared_main("stv", scheme)


if __name__ == "__main__":
    main()
