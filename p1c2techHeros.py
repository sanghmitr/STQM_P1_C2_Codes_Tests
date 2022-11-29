import datetime
import itertools
from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pylab import rcParams
from pymongo import MongoClient

cluster = MongoClient("mongodb://localhost:27017")

db = cluster["smartshark"]

projectCollections = db["project"]
commit_with_projectInfo_Collection = db['commit_with_project_info']
file_action_Collection = db["file_action"]

totalDevlopersInProject = 0
developerCommits = defaultdict(set)


def getTotalDevelopers(projectName):
    projectDetails = projectCollections.find_one({"name": projectName})
    committersWithCount = commit_with_projectInfo_Collection.aggregate([
        {"$match": {"project_id_info.project_id": projectDetails['_id']}},
        {"$group": {"_id": "$author_id", "commitCount": {"$sum": 1}}}
    ])

    developersCommitCount = []
    for entry in committersWithCount:
        developersCommitCount.append([entry['_id'], entry['commitCount']])

    return len(developersCommitCount)


def findHeroDevsBasedOnCommits(projectName):
    projectDetails = projectCollections.find_one({"name": projectName})
    # print(projectDetails)
    # Reference of commit_with_project_info collection

    committersWithCount = commit_with_projectInfo_Collection.aggregate([
        {"$match": {"project_id_info.project_id": projectDetails['_id']}},
        {"$group": {"_id": "$author_id", "commitCount": {"$sum": 1}}}
    ])

    # Number of commits done by each developer in Kafka Project

    developersCommitCount = []
    for entry in committersWithCount:
        developersCommitCount.append([entry['_id'], entry['commitCount']])
    # print(entry['_id'], " -> ", entry['count'])

    developersCommitCount.sort(key=lambda x: x[1], reverse=True)

    totalCommitsInProject = commit_with_projectInfo_Collection.count_documents(
        {"project_id_info.project_id": projectDetails['_id']})
    print("Total Number of commits in Project :- ", totalCommitsInProject)

    percent80_commits = totalCommitsInProject * 0.8

    tempCommit = 0
    heroDevsBasedOnCommit = set()
    i = 0
    while (tempCommit <= percent80_commits):
        tempCommit += int(developersCommitCount[i][1])
        heroDevsBasedOnCommit.add(developersCommitCount[i][0])
        i += 1

    # print(heroDevsBasedOnCommit)
    totalDevs = getTotalDevelopers(projectName)

    print("Hero Developers : ", len(heroDevsBasedOnCommit))
    print("Total Developers in Project : ", totalDevs)
    print("Hero developer in Project by %: ", (len(heroDevsBasedOnCommit) / totalDevs) * 100)
    print("------------------------------------------------------------")

    return heroDevsBasedOnCommit


"""**Task - 2 : Find the number of files updated by each Developer**
Find list of commits done by each developer
"""


def findHeroDevsBasedOnFiles(projectName):
    projectDetails = projectCollections.find_one({"name": projectName})
    # Make data structure ->
    # {
    #     developer1 : [commit_1, commit_2, ....],
    #     developer2 : [commit_1, commit_2, ....],
    # }

    commits = commit_with_projectInfo_Collection.find({"project_id_info.project_id": projectDetails['_id']})
    for commit in commits:
        # print(commit)
        developerCommits[commit['author_id']].add(commit['_id'])

    # totalFileModifications = file_action_Collection.count_documents({})
    # print(totalFileModifications)

    # Number of files updated by each developer

    developerFilesDict = defaultdict(int)

    for developerId, commitList in developerCommits.items():
        for commitId in commitList:
            # print(commitId)
            no_of_files_Modified = file_action_Collection.count_documents({"commit_id": {"$eq": commitId}})
            developerFilesDict[developerId] += no_of_files_Modified

    # print(developerFilesDict)

    developerFilesCount = list(developerFilesDict.items())
    developerFilesCount.sort(key=lambda x: x[1], reverse=True)

    """Total File Modifications in Project"""

    totalFileModifications = 0
    for entry in developerFilesCount:
        totalFileModifications += entry[1]

    print("Total File modifications in Project : ", totalFileModifications)

    percent80_Files = totalFileModifications * 0.8

    tempFiles = 0
    heroDevsBasedOnFiles = set()
    i = 0
    while (tempFiles <= percent80_Files):
        tempFiles += int(developerFilesCount[i][1])
        heroDevsBasedOnFiles.add(developerFilesCount[i][0])
        i += 1

    # print(heroDevsBasedOnFiles)
    totalDevs = getTotalDevelopers(projectName)

    print("Hero Developers : ", len(heroDevsBasedOnFiles))
    print("Total Developers in Project : ", totalDevs)
    print("Hero developer in project by % : ", (len(heroDevsBasedOnFiles) / totalDevs) * 100)
    print("--------------------------------------------------")

    return heroDevsBasedOnFiles


"""**Total Number of Lines Added overall (Only Lines added are considered)**

"""


def findHeroDevsBasedOnLines(projectName):
    # Make data structure ->
    # {
    #     developer1 : numberOfLinesAdded,
    #     developer2 : numberOfLinesAdded,
    # }

    queryOutput = file_action_Collection.aggregate([
        {
            "$group": {
                "_id": {},
                "sum_lines_added": {
                    "$sum": "$lines_added"
                }
            }
        },
        {
            "$project": {
                "sum_lines_added": 1,
                "_id": 0
            }
        }])

    totalLinesModifications = 0
    for data in queryOutput:
        totalLinesModifications = data['sum_lines_added']

    # print(totalLinesModifications)

    """Find number of lines changed by each developer in each commmit"""

    developerLinesDict = defaultdict(int)

    for developerId, commitList in developerCommits.items():
        count = 0
        for commitId in commitList:
            temp = file_action_Collection.aggregate([{
                "$match": {
                    "commit_id": commitId
                }
            }, {
                "$group": {
                    "_id": {},
                    "sum_lines_added": {
                        "$sum": "$lines_added"
                    }
                }
            }, {
                "$project": {
                    "sum_lines_added": 1,
                    "_id": 0
                }
            }])

            for data in temp:
                count += data['sum_lines_added']

        developerLinesDict[developerId] = count

    developerLinesCount = list(developerLinesDict.items())

    developerLinesCount.sort(key=lambda x: x[1], reverse=True)

    """Total Lines added in Project Kafka"""

    totalLinesWritten = 0
    for devId, linescount in developerLinesDict.items():
        totalLinesWritten += linescount

    print("Total lines written in project : ", totalLinesWritten)

    percent80_Lines = totalLinesWritten * 0.8

    tempLines = 0
    heroDevsBasedOnLines = set()
    i = 0
    while (tempLines <= percent80_Lines):
        tempLines += int(developerLinesCount[i][1])
        heroDevsBasedOnLines.add(developerLinesCount[i][0])
        i += 1

    # print(heroDevsBasedOnLines)

    totalDevs = getTotalDevelopers(projectName)
    print("Hero Developers : ", len(heroDevsBasedOnLines))
    print("Total Developers in project : ", totalDevs)
    print("Hero developer in project by % : ", (len(heroDevsBasedOnLines) / totalDevs) * 100)
    print("--------------------------------------------------")

    return heroDevsBasedOnLines


def findOverallTechnicalDevelopers(projectName):
    heroDevsBasedOnCommit = findHeroDevsBasedOnCommits(projectName)
    heroDevsBasedOnFile = findHeroDevsBasedOnFiles(projectName)
    heroDevsBasedOnLine = findHeroDevsBasedOnLines(projectName)
    # """Apply set intersection to find overall technical heros"""
    ans = dict()
    ans["heroDevsBasedOnCommit"] = len(heroDevsBasedOnCommit)
    ans["heroDevsBasedOnFile"] = len(heroDevsBasedOnFile)
    ans["heroDevsBasedOnLine"] = len(heroDevsBasedOnLine)

    heroDevsOverall = heroDevsBasedOnLine.intersection(heroDevsBasedOnCommit, heroDevsBasedOnFile)
    print("Overall Technical Heros : ", len(heroDevsOverall))
    print("------------------------------------------")
    # print(heroDevsOverall)
    ans["heroDevsOverall"] = len(heroDevsOverall)
    ans["heroDevsList"] = heroDevsOverall
    return ans
    # return heroDevsOverall

print("Overall Devs:", findOverallTechnicalDevelopers("kafka"))

