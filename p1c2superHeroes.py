from pymongo import MongoClient

from p1c2techHeros import findOverallTechnicalDevelopers
from p1c2socialHeros import  findSocialHerosBasedOnComments

cluster = MongoClient("mongodb://localhost:27017")
db = cluster["smartshark"]
project = db['project']

def findSuperHeros(projectName):
    techHeros = findOverallTechnicalDevelopers(projectName)
    socialHeroes = findSocialHerosBasedOnComments(projectName)

    superHeros = techHeros["heroDevsList"].intersection(socialHeroes["social_hero_list"])
    print("Total number of superheros in Project ", projectName, " : ", len(superHeros))
    # print(superHeros)
    return superHeros

print(findSuperHeros("kafka"))



