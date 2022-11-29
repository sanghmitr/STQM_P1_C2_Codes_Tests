import pytest
from bson import ObjectId

from p1c2newcomers import findNewComers

kafka_new_comers = {ObjectId('636529d6e9a99c9121bb945b'), ObjectId('636529d6e9a99c9121bc9f1f'), ObjectId('636529d6e9a99c9121bc9f1a'), ObjectId('636529d6e9a99c9121bbedb5'), ObjectId('636529d6e9a99c9121bba37f'), ObjectId('636529d6e9a99c9121bc9f21'), ObjectId('636529d6e9a99c9121bc982b'), ObjectId('636529d5e9a99c9121bb2774'), ObjectId('636529d6e9a99c9121bc9108'), ObjectId('636529d6e9a99c9121bc9117'), ObjectId('636529d6e9a99c9121bc9118'), ObjectId('636529d6e9a99c9121bc90f1'), ObjectId('636529d6e9a99c9121bc5fc9'), ObjectId('636529d6e9a99c9121bc9f1e'), ObjectId('636529d6e9a99c9121bc9f20'), ObjectId('636529d6e9a99c9121bc9114'), ObjectId('636529d6e9a99c9121bc9830'), ObjectId('636529d6e9a99c9121bbcfed'), ObjectId('636529d6e9a99c9121bc9831'), ObjectId('636529d6e9a99c9121bc92a5'), ObjectId('636529d5e9a99c9121bb43f5'), ObjectId('636529d6e9a99c9121bc9f22'), ObjectId('636529d6e9a99c9121bc92a4'), ObjectId('636529d5e9a99c9121bb2f16'), ObjectId('636529d6e9a99c9121bc97fd'), ObjectId('636529d6e9a99c9121bc9f1b'), ObjectId('636529d6e9a99c9121bc911b'), ObjectId('636529d6e9a99c9121bc982c'), ObjectId('636529d6e9a99c9121bc92a1'), ObjectId('636529d6e9a99c9121bc92ae'), ObjectId('636529d6e9a99c9121bbb43a')}
pig_new_comers = {ObjectId('636529d6e9a99c9121bc4b16'), ObjectId('636529d6e9a99c9121bc9efc')}

@pytest.mark.parametrize("project_name, expected_output", [("kafka", kafka_new_comers), ("pig", pig_new_comers)])
def test_new_comers(project_name, expected_output):
    assert expected_output == findNewComers(project_name)