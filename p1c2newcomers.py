from datetime import datetime
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient
from dateutil.parser import parse

cluster = MongoClient("mongodb://localhost:27017")
db = cluster["smartshark"]
project = db['project']
commit_with_project_info = db['commit_with_project_info']


def findNewComers(projectName):
    projectDetails = project.find_one({"name": projectName})

    startDate , endDate = getDates(projectName)
    commitsIn6MonthsDevs = commit_with_project_info.find({
        "project_id_info.project_id": projectDetails['_id'],
        "committer_date": {
            "$gte": startDate,
            "$lte": endDate
        }}, {"author_id": 1})

    SixMonthsDevs = set()
    for a in commitsIn6MonthsDevs:
        SixMonthsDevs.add(a['author_id'])

    commitsIn3Years = commit_with_project_info.find({
        "project_id_info.project_id": projectDetails['_id'],
        "committer_date": {
            "$lte": startDate
        }}, {"author_id": 1})
    first3YearDevs = set()
    for a in commitsIn3Years:
        first3YearDevs.add(a['author_id'])

    newComers = SixMonthsDevs.difference(first3YearDevs)

    # print("Total Number of Experienced Devs : ", len(first3YearDevs))
    # print("Total Number of Newcomers along with experienced Devs : ", len(SixMonthsDevs))
    # print("Total Number of NewComers : ", len(newComers))
    # print("--------------------------\nNew comers\n--------------------------")
    # input("Press any key to continue")
    # for auto in newComers:
    #     print(auto)

    return newComers

def getDates(projectName):
    startDate = commit_with_project_info.find({"project_name_info.name": projectName})\
        .sort([("committer_date",1)]).limit(1)
    sDate = datetime.today()
    eDate = datetime.today()
    for a in startDate:
        threeYearsDate = a["committer_date"] + relativedelta(years=3)
        sDate = threeYearsDate
        eDate = sDate + relativedelta(months=6)

    return sDate, eDate

# projectName = input("Enter project name: ")
print("Newcomers in project:", len(findNewComers("kafka")))