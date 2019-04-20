### >> Settings :
Here you can find all the **settings.py** variable to interact with **neo4j_for_django**.
Note that all the parameters created or updated by **neo4j_for_django** are prefixed by **N4D**.

---
<br/>

```python
set_neo4j_for_django_settings_on(locals())


############################################################################
#                        neo4j_for_django's variables                      #
############################################################################


################
# N4D DATABASE #
################



# This parameter defines the attempts number where the application will retry to establish the initial connection with
# the Neo4j database (each attempt is separated by 1 second).
# It prevents failed when the database takes a long time to start or restart.
# Explanations here :
# https://neo4j.com/docs/operations-manual/3.0/deployment/post-installation/#post-installation-wait-for-start
N4D_INITIAL_CONNECTION_ATTEMPTS_NUMBER = 8



# Neo4j authentification :
N4D_DATABASE_URI = "bolt://localhost:7687"


N4D_DATABASE_ID = 'neo4j'


N4D_DATABASE_PASSWORD = '1234'



# Encrypting trafic between the Neo4j driver and the Neo4j instance.
# Explanations here : https://neo4j.com/docs/developer-manual/3.0/drivers/driver/#driver-authentication-encryption
N4D_DATABASE_ENCRYPTED = True


# Verification against "man-in-the-middle" attack.
# Explanations : https://neo4j.com/docs/developer-manual/3.0/drivers/driver/#_trust
# Choices :
# 0 : TRUST_ON_FIRST_USE     (Deprecated)
# 1 : TRUST_SIGNED_CERTIFICATES     (Deprecated)
# 2 : TRUST_ALL_CERTIFICATES
# 3 : TRUST_CUSTOM_CA_SIGNED_CERTIFICATES
# 4 : TRUST_SYSTEM_CA_SIGNED_CERTIFICATES
# 5 : TRUST_DEFAULT = TRUST_ALL_CERTIFICATES
N4D_DATABASE_TRUST = 2



# These parameters define the transactions modalities (after the establishment of the initial connection)
# Explanations here : https://neo4j.com/docs/api/python-driver/current/driver.html#max-connection-lifetime
N4D_DATABASE_MAX_CONNECTION_LIFETIME = 60 * 60


N4D_DATABASE_MAX_CONNECTION_POOL_SIZE = 50


N4D_DATABASE_CONNECTION_ACQUISITION = 60


N4D_DATABASE_CONNECTION_TIMEOUT = 15


N4D_DATABASE_MAX_RETRY_TIME = 15




################
# N4D SESSIONS #
################


N4D_SESSION_CHANGE_ON_EVERY_REQUEST = False


SESSION_ENGINE = 'neo4j_for_django.contrib.sessions.backends.db'


SESSION_SERIALIZER = 'neo4j_for_django.contrib.sessions.serializers.JSONSerializer'  # modified


# You can define all the session variables like with the native Django package.
# Example
SESSION_COOKIE_AGE = 60 * 60 * 24 


######################
# N4D AUTHENTICATION #
######################


N4D_LOGIN_URL = '/blog/login/'


N4D_HOME_PAGE_URL = '/blog/articles/'


N4D_LOGIN_REDIRECT_URL = '/blog/articles/'


N4D_LOGOUT_REDIRECT_URL = None # TODO



##############
# N4D PEPPER #
##############


N4D_PEPPER_1 = 'e3cccVk8m^jwK2w/&g1:wFE^1'


N4D_PEPPER_2 = 'E^7vV!Sm2:K!yDJ4oebOCQM*7gGdR%?,W.'
```
<br/>
<br/>
<br/>