from pymongo import MongoClient
from p1c2techHeros import findOverallTechnicalDevelopers
from p1c2socialHeros import findSocialHerosBasedOnComments


cluster = MongoClient("mongodb://localhost:27017")
db = cluster["smartshark"]
projectCollection = db["project"]
commit_with_projectInfo_Collection = db['commit_with_project_info']

def findMedian(l):
    # print("Developer comment length : ", len(l))
    mid = len(l) // 2
    median = (l[mid][1] + l[~mid][1]) / 2
    return median

def findSocioTechnicalHeros(projectName):
    socialHeroes = findSocialHerosBasedOnComments(projectName)
    print("Social Heroes : ", len(socialHeroes["social_hero_list"]))

    projectDetails = projectCollection.find_one({"name": projectName})
    committersWithCount = commit_with_projectInfo_Collection.aggregate([
        {"$match": {"project_id_info.project_id": projectDetails['_id']}},
        {"$group": {"_id": "$author_id", "commitCount": {"$sum": 1}}}
    ])

    # Number of commits done by each developer in Project
    developersCommitCount = []
    for entry in committersWithCount:
        developersCommitCount.append([entry['_id'], entry['commitCount']])
    # print(entry['_id'], " -> ", entry['count'])

    developersCommitCount.sort(key=lambda x: x[1], reverse=True)

    median = findMedian(developersCommitCount)
    print("---------------------------------------")
    print("Median number of commits :- ", median)
    print("---------------------------------------")

    technicalHerosAboveMedian = set()

    i = 0
    while developersCommitCount[i][1] > median and i < len(developersCommitCount):
        technicalHerosAboveMedian.add(developersCommitCount[i][0])
        i += 1

    # print(socialHerosAboveMedian)
    socioTechnicalHeros = technicalHerosAboveMedian.intersection(socialHeroes["social_hero_list"])

    print("Total number of socioTechnical Heros: ", len(socioTechnicalHeros))
    # print(socioTechnicalHeros)
    return socioTechnicalHeros

print(findSocioTechnicalHeros("kafka"))
