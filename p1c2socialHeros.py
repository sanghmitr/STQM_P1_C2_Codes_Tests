from collections import defaultdict
from datetime import datetime

from pymongo import MongoClient

cluster = MongoClient("mongodb://localhost:27017")
db = cluster["smartshark"]
project = db['project']
comments_with_issue_and_project_info_collection = db["comments_with_issue_and_project_info"]
issue_with_project_info_collection = db['issue_with_project_info']


def findSocialHerosBasedOnComments(projectName):
    projectDetails = project.find_one({"name": projectName})
    comments = comments_with_issue_and_project_info_collection.find(
        {
            "issue_info.project_id_info.project_id": projectDetails['_id']
        },
        {"author_id": 1}
    )

    authorCommentCountDict = defaultdict(int)

    for comment in comments:
        authorCommentCountDict[comment['author_id']] += 1
    totalCommentsInProject = comments_with_issue_and_project_info_collection.count_documents(
        {"issue_info.project_id_info.project_id": projectDetails['_id']})

    # Sort the dev lists
    developerCommentCounts = list(authorCommentCountDict.items())

    developerCommentCounts.sort(key=lambda x: x[1], reverse=True)

    totalSum = 0
    targetCount = totalCommentsInProject * 0.8
    i = 0
    heroDevs = set()
    while (totalSum <= targetCount):
        totalSum += developerCommentCounts[i][1]
        i += 1
        heroDevs.add(developerCommentCounts[i][0])

    totalDevs = issue_with_project_info_collection.count_documents({"project_id_info.project_id": projectDetails['_id'],
                                                                    "assignee_id": {"$exists": True}})
    ans = dict()
    ans["social_hero_devs"] = len(heroDevs)
    ans["total_devs"] = totalDevs
    ans["social_hero_dev_percentage"] = (len(heroDevs) / totalDevs) * 100
    ans["social_hero_list"] = heroDevs
    # print("Hero Devs : ", len(heroDevs))
    # print("Total devs in Kafka : ", totalDevs)
    # print("Dev percentage : ", (len(heroDevs) / totalDevs) * 100)
    return ans

print(findSocialHerosBasedOnComments("kafka"))

