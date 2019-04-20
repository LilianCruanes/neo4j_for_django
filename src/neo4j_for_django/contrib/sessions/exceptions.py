from neo4j_for_django.db.exceptions import N4DNodeError


class N4DSessionDoesNotExist(N4DNodeError):
    pass


class N4DSessionDoesNotHaveData(N4DNodeError):
    pass
