from collections import Counter
from typing import Hashable

from types1 import Ballot

def pairwise(ballots: list[Ballot]) -> dict[Hashable, dict[Hashable, int]]:
    candidates: set[Hashable] = set()
    for ballot in ballots:
        for candidate in ballot.ranking:
            candidates.add(candidate)
    pairwise: dict[Hashable, dict[Hashable, int]] = {}
    for candidateA in candidates:
        pairwise[candidateA] = {}
        for candidateB in candidates:
            pairwise[candidateA][candidateB] = 0
    for ballot in ballots:
        for rankA, candidateA in enumerate(ballot.ranking):
            for rankB, candidateB in enumerate(ballot.ranking):
                if rankA < rankB:
                    pairwise[candidateA][candidateB] += ballot.tally
                    pairwise[candidateB][candidateA] -= ballot.tally
            for candidateB in candidates:
                if candidateB not in ballot.ranking:
                    pairwise[candidateA][candidateB] += ballot.tally
                    pairwise[candidateB][candidateA] -= ballot.tally
    return pairwise


def condorcet(ballots: list[Ballot]) -> Hashable:
    h2h = pairwise(ballots)
    candidates = h2h.keys()
    for candidateA in candidates:
        winner = True
        for candidateB in candidates:
            result = h2h[candidateA][candidateB]
            if result <= 0 and candidateA != candidateB:
                winner = False
        if winner:
            return candidateA
    return


def smith_set(ballots: list[Ballot]) -> set[Hashable]:
    h2h = pairwise(ballots)
    cScores: dict[Hashable, float] = {}
    candidates = h2h.keys()
    for candidateA in candidates:
        cScores[candidateA] = -1 / 2
        for candidateB in candidates:
            result = h2h[candidateA][candidateB]
            if result > 0:
                cScores[candidateA] += 1
            elif result == 0:
                cScores[candidateA] += 1 / 2
    cScoresSorted = dict(
        sorted(cScores.items(), key=lambda item: item[1], reverse=True)
    )
    smith = set()
    lowestSmithScore = cScoresSorted[next(iter(cScoresSorted))]
    candidateAdded = True
    while candidateAdded:
        candidateAdded = False
        for candidate in candidates:
            if candidate not in smith and cScores[candidate] >= lowestSmithScore:
                candidateAdded = True
                smith.add(candidate)
        toAdd = []
        for candidateA in smith:
            for candidateB in candidates:
                if h2h[candidateA][candidateB] <= 0 and candidateB not in smith:
                    candidateAdded = True
                    toAdd.append(candidateB)
                    lowestSmithScore = min(lowestSmithScore, cScores[candidateB])
        for candidate in toAdd:
            smith.add(candidate)
    return smith

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

def clear_empty(ballots: list[Ballot]):
    notEmpty = []
    for ballot in ballots:
        if (ballot.tally != 0):
            notEmpty.append(ballot)
    return notEmpty

print([
            {"ranking": [0, 2, 1], "count": 3},
            {"ranking": [1, 2, 0], "count": 3},
            {"ranking": [2, 0, 1], "count": 1},
            {"ranking": [0, 1, 2], "count": 0},
            {"ranking": [1, 0, 2], "count": 3},
        ])

print(eliminate_candidate([
            {"ranking": [0, 2, 1], "count": 3},
            {"ranking": [1, 2, 0], "count": 3},
            {"ranking": [2, 0, 1], "count": 1},
            {"ranking": [0, 1, 2], "count": 0},
            {"ranking": [1, 0, 2], "count": 3},
        ], 1))

print(count_first([
            {"ranking": [0, 2, 1], "count": 3},
            {"ranking": [1, 2, 0], "count": 3},
            {"ranking": [2, 0, 1], "count": 1},
            {"ranking": [0, 1, 2], "count": 0},
            {"ranking": [1, 0, 2], "count": 3},
        ]))

print(
    smith_set(
        [
            {"ranking": [0, 2, 1], "count": 3},
            {"ranking": [1, 2, 0], "count": 3},
            {"ranking": [2, 0, 1], "count": 1},
            {"ranking": [0, 1, 2], "count": 0},
            {"ranking": [1, 0, 2], "count": 3},
        ]
    )
)
