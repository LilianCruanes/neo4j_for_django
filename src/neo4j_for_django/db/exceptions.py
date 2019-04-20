

# Base neo4j_for_django error
class neo4j_for_djangoError(BaseException):
    pass


#  Base neo4j_for_django error --> Client error
class N4DClientError(neo4j_for_djangoError):
    pass


#  Base neo4j_for_django error --> Client error --> Node error
class N4DNodeError(N4DClientError):
    pass


#  Base neo4j_for_django error --> Client error --> Node error --> Node initialization error --> labels
class N4DNodeLabelsInitializationError(N4DNodeError):
    pass


# Base neo4j_for_django error --> Client error --> Connection error
class N4DConnectionError(N4DClientError):
    pass


# Base neo4j_for_django error --> Client error --> Connection warning
class N4DConnectionWarning(N4DClientError, Warning):
    pass


# Base neo4j_for_django error --> Client error --> Transaction error
class N4DTransactionError(N4DClientError):
    pass


# Base neo4j_for_django error --> Client error --> Transaction error --> Transaction type error
class N4DTransactionTypeError(N4DTransactionError):
    pass


# Base neo4j_for_django error --> Client error --> Transaction error --> Transaction conflict error
class N4DTransactionConflictError(N4DTransactionError):
    pass


# Base neo4j_for_django error --> Client error --> Session error
class N4DSessionError(N4DClientError):
    pass


#  Base neo4j_for_django error --> Database error
class N4DDatabaseError(neo4j_for_djangoError):
    pass


#  Base neo4j_for_django error --> Database error --> field error
class N4DFieldError(N4DDatabaseError):
    pass


#  Base neo4j_for_django error --> Database error --> field error --> required constraint error
class N4DRequiredConstraintError(N4DFieldError):
    pass


#  Base neo4j_for_django error --> Database error --> unique constraint error
class N4DUniqueConstraintError(N4DFieldError):
    pass


#  Base neo4j_for_django error --> Database error --> attribute error
class N4DAttributeError(N4DFieldError):
    pass