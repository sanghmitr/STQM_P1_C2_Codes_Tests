from datetime import datetime
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient
from dateutil.parser import parse
from NewComers import findNewComers
from technical_heroes import findHeroDevsBasedOnCommits
from technical_heroes import findHeroDevsBasedOnFiles
from technical_heroes import findHeroDevsBasedOnLines


cluster = MongoClient("mongodb://localhost:27017")
db = cluster["smartshark"]
project = db['project']
commit_with_project_info = db['commit_with_project_info']

time = 3
projectName = "kafka"

newComers = findNewComers(projectName)
longTermContributors = set()

def findLongTermContributors(projectName, T):
    for auto in newComers:
        startDate = commit_with_project_info.find({"project_name_info.name": projectName, "author_id": auto}) \
                    .sort([("committer_date", 1)]).limit(1)
        endDate = commit_with_project_info.find({"project_name_info.name": projectName, "author_id": auto}) \
                    .sort([("committer_date", -1)]).limit(1)

        sDate = datetime.today()
        eDate = datetime.today()

        for a in startDate:
            sDate = a["committer_date"]
        for b in endDate:
            eDate = b["committer_date"]
        if eDate >= sDate + relativedelta(years=T):
            longTermContributors.add(auto)

findLongTermContributors("kafka", time)

heroDevsCommits = findHeroDevsBasedOnCommits(projectName)
heroDevsFiles = findHeroDevsBasedOnFiles(projectName)
heroDevsLines = findHeroDevsBasedOnLines(projectName)

LTC_to_hero = heroDevsCommits.intersection(heroDevsFiles, heroDevsLines, longTermContributors)


print("New Comers that become LTC given time", time, "years:", len(longTermContributors), "\tOut of Total Newcomers:", len(newComers))
print("Number of Long term Contributors that become Hero later:", len(LTC_to_hero))


