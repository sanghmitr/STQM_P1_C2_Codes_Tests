import datetime
import itertools
from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pylab import rcParams
from pymongo import MongoClient
from p1c2techHeros import findOverallTechnicalDevelopers

# import socialheroes


cluster = MongoClient("mongodb://localhost:27017")
db = cluster["smartshark"]
projectCollection = db["project"]
commit_with_projectInfo_Collection = db['commit_with_project_info']
file_action_Collection = db["file_action"]
comments_with_issue_and_project_info_collection = db["comments_with_issue_and_project_info"]
issue_with_project_info_collection = db['issue_with_project_info']


def findMedian(l):
    # print("Developer comment length : ", len(l))
    mid = len(l) // 2
    median = (l[mid][1] + l[~mid][1]) / 2
    return median


def findTechnoSocialHerosBasedOnComments(projectName):
    projectDetails = projectCollection.find_one({"name": projectName})
    # print(projectDetails)
    techHeros = findOverallTechnicalDevelopers(projectName)

    # Social Contribution
    comments = comments_with_issue_and_project_info_collection.find(
        {
            "issue_info.project_id_info.project_id": projectDetails['_id']
        },
        {"author_id": 1}
    )

    authorCommentCountDict = defaultdict(int)
    for comment in comments:
        authorCommentCountDict[comment['author_id']] += 1
    # total number of comments in project
    # totalCommentsInProject = comments_with_issue_and_project_info_collection.count_documents({"issue_info.project_id_info.project_id":projectDetails['_id']})
    # print(totalCommentsInProject)

    # Sort the dev lists
    developerCommentCounts = list(authorCommentCountDict.items())
    developerCommentCounts.sort(key=lambda x: x[1], reverse=True)

    # print("Developer Comment Count list :- ", developerCommentCounts)
    median = findMedian(developerCommentCounts)
    print("---------------------------------------")
    print("Median number of comments :- ", median)
    print("---------------------------------------")

    socialHerosAboveMedian = set()

    i = 0
    while developerCommentCounts[i][1] > median and i < len(developerCommentCounts):
        socialHerosAboveMedian.add(developerCommentCounts[i][0])
        i += 1

    # print(socialHerosAboveMedian)
    technoSocialheros = socialHerosAboveMedian.intersection(techHeros["heroDevsList"])

    print("Total number of TechnoSocial Heros: ", len(technoSocialheros))
    print(technoSocialheros)