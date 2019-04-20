def set_neo4j_for_django_settings_on(root_settings):
    """
    This function overwrite many settings variables from the project's settings.py file, in order
    to add the neo4j_for_django modules to the project but also to make compatible the django project with neo4j_for_django.
    :param root_settings: The locals() dict of the project settings.py file
    """

    # Remove the native auth module and set the neo4j_for_django one.
    try:
        INSTALLED_APPS = root_settings['INSTALLED_APPS']

    except KeyError:
        root_settings['INSTALLED_APPS'] = ['neo4j_for_django.contrib.auth', ]

    else:
        if 'django.contrib.auth' in INSTALLED_APPS:
            INSTALLED_APPS.remove('django.contrib.auth')
            INSTALLED_APPS.insert(0, 'neo4j_for_django.contrib.auth')
        else:
            pass
            INSTALLED_APPS.insert(0, 'neo4j_for_django.contrib.auth')

    # Remove the native admin module and set the neo4j_for_django one.
    try:
        INSTALLED_APPS = root_settings['INSTALLED_APPS']

    except KeyError:
        pass
        # root_settings['INSTALLED_APPS'] = ['neo4j_for_django.contrib.admin', ] # TODO

    else:
        if 'django.contrib.admin' in INSTALLED_APPS:
            INSTALLED_APPS.remove('django.contrib.admin')
            # INSTALLED_APPS.insert(0, 'neo4j_for_django.contrib.admin') # TODO
        else:
            pass
            # INSTALLED_APPS.insert(0, 'neo4j_for_django.contrib.admin') # TODO

    # Remove the native contenttypes module and set the neo4j_for_django one.
    try:
        INSTALLED_APPS = root_settings['INSTALLED_APPS']

    except KeyError:
        pass
        # root_settings['INSTALLED_APPS'] = ['neo4j_for_django.contrib.contenttypes', ]

    else:
        if 'django.contrib.contenttypes' in INSTALLED_APPS:
            INSTALLED_APPS.remove('django.contrib.contenttypes')
            # INSTALLED_APPS.insert(0, 'neo4j_for_django.contrib.contenttypes')
        else:
            pass
            # INSTALLED_APPS.insert(0, 'neo4j_for_django.contrib.contenttypes')

    # Remove the native sessions module and set the neo4j_for_django one.
    try:
        INSTALLED_APPS = root_settings['INSTALLED_APPS']

    except KeyError:
        root_settings['INSTALLED_APPS'] = ['neo4j_for_django.contrib.sessions', ]

    else:
        if 'django.contrib.sessions' in INSTALLED_APPS:
            INSTALLED_APPS.remove('django.contrib.sessions')
            INSTALLED_APPS.insert(0, 'neo4j_for_django.contrib.sessions')
        else:
            pass
            INSTALLED_APPS.insert(0, 'neo4j_for_django.contrib.sessions')

    # Add the neo4j_for_django database module.
    try:
        INSTALLED_APPS = root_settings['INSTALLED_APPS']

    except KeyError:
        root_settings['INSTALLED_APPS'] = ['neo4j_for_django.db', ]

    else:
        INSTALLED_APPS.insert(0, 'neo4j_for_django.db')

    # Remove the native auth middleware and set the neo4j_for_django one.
    try:
        MIDDLEWARE = root_settings['MIDDLEWARE']

    except KeyError:
        root_settings['MIDDLEWARE'] = ['django.contrib.auth.middleware.AuthenticationMiddleware', ]

    else:
        if 'django.contrib.auth.middleware.AuthenticationMiddleware' in MIDDLEWARE:
            MIDDLEWARE.remove('django.contrib.auth.middleware.AuthenticationMiddleware')
            MIDDLEWARE.insert(2, 'neo4j_for_django.contrib.auth.middleware.AuthenticationMiddleware')
        else:
            pass
            MIDDLEWARE.insert(2, 'neo4j_for_django.contrib.auth.middleware.AuthenticationMiddleware')

    # Remove the native sessions middleware and set the neo4j_for_django one.
    try:
        MIDDLEWARE = root_settings['MIDDLEWARE']

    except KeyError:
        root_settings['MIDDLEWARE'] = ['neo4j_for_django.contrib.sessions.middleware.SessionMiddleware', ]

    else:
        if 'django.contrib.sessions.middleware.SessionMiddleware' in MIDDLEWARE:
            MIDDLEWARE.remove('django.contrib.sessions.middleware.SessionMiddleware')
            MIDDLEWARE.insert(1, 'neo4j_for_django.contrib.sessions.middleware.SessionMiddleware')
        else:
            pass
            MIDDLEWARE.insert(1, 'neo4j_for_django.contrib.sessions.middleware.SessionMiddleware')

    # Remove the native auth context processcors.
    try:
        TEMPLATES_context_processors = root_settings['TEMPLATES'][0]['OPTIONS']['context_processors']

    except KeyError:
        root_settings['TEMPLATES']['OPTIONS']['context_processors'] = ['neo4j_for_django.contrib.auth.context_processors.user_context_processors',]

    else:
        if 'django.contrib.auth.context_processors.auth' in TEMPLATES_context_processors:
            TEMPLATES_context_processors.remove('django.contrib.auth.context_processors.auth')
            TEMPLATES_context_processors.insert(0, 'neo4j_for_django.contrib.auth.context_processors.user_context_processors')
        else:
            pass
            TEMPLATES_context_processors.insert(0, 'neo4j_for_django.contrib.auth.context_processors.user_context_processors')

    ##################
    # AUTHENTICATION #
    ##################

    # Remove the native auth backends config.
    root_settings['AUTH_USER_MODEL'] = None
    root_settings['AUTHENTICATION_BACKENDS'] = []
    root_settings['AUTH_PASSWORD_VALIDATORS'] = []

    ############################################################################
    #                        neo4j_for_django's variables                      #
    ############################################################################

    ################
    # N4D DATABASE #
    ################

    # This parameter defines the attempts number where the application will retry to establish the initial connection
    # with the Neo4j database (each attempt is separated by 1 second).
    # It prevents failed when the database takes a long time to start or restart.
    # Explanations here :
    # https://neo4j.com/docs/operations-manual/3.0/deployment/post-installation/#post-installation-wait-for-start
    root_settings['N4D_INITIAL_CONNECTION_ATTEMPTS_NUMBER'] = 5

    # Neo4j authentification :
    root_settings['N4D_DATABASE_URI'] = "bolt://localhost:7687"

    root_settings['N4D_DATABASE_ID'] = 'neo4j'

    root_settings['N4D_DATABASE_PASSWORD'] = '1234'

    # Encrypting trafic between the Neo4j driver and the Neo4j instance.
    # Explanations here : https://neo4j.com/docs/developer-manual/3.0/drivers/driver/#driver-authentication-encryption
    root_settings['N4D_DATABASE_ENCRYPTED'] = True

    # Verification against "man-in-the-middle" attack.
    # Explanations : https://neo4j.com/docs/developer-manual/3.0/drivers/driver/#_trust
    # Choices :
    # 0 : TRUST_ON_FIRST_USE     (Deprecated)
    # 1 : TRUST_SIGNED_CERTIFICATES     (Deprecated)
    # 2 : TRUST_ALL_CERTIFICATES
    # 3 : TRUST_CUSTOM_CA_SIGNED_CERTIFICATES
    # 4 : TRUST_SYSTEM_CA_SIGNED_CERTIFICATES
    # 5 : TRUST_DEFAULT = TRUST_ALL_CERTIFICATES
    root_settings['N4D_DATABASE_TRUST'] = 2

    # These parameters define the transactions modalities (after the establishment of the initial connection)
    root_settings['N4D_DATABASE_MAX_CONNECTION_LIFETIME'] = 60 * 60

    root_settings['N4D_DATABASE_MAX_CONNECTION_POOL_SIZE'] = 50

    root_settings['N4D_DATABASE_CONNECTION_ACQUISITION'] = 60

    root_settings['N4D_DATABASE_CONNECTION_TIMEOUT'] = 15

    root_settings['N4D_DATABASE_MAX_RETRY_TIME'] = 15

    ################
    # N4D SESSIONS #
    ################

    root_settings['N4D_SESSION_CHANGE_ON_EVERY_REQUEST'] = False

    root_settings['SESSION_ENGINE'] = 'neo4j_for_django.contrib.sessions.backends.db'  # modified

    root_settings['SESSION_SERIALIZER'] = 'neo4j_for_django.contrib.sessions.serializers.JSONSerializer'  # modified

    ######################
    # N4D AUTHENTICATION #
    ######################

    root_settings['N4D_LOGIN_URL'] = '/blog/login/'

    root_settings['N4D_LOGIN_REDIRECT_URL'] = '/blog/articles/'

    root_settings['N4D_LOGOUT_REDIRECT_URL'] = None  # TODO

    ##############
    # N4D PEPPER #
    ##############

    root_settings['N4D_PEPPER_1'] = None

    root_settings['N4D_PEPPER_2'] = None

    ############################################################################
    #                      neo4j_for_django used variables                     #
    ############################################################################

    # The first hasher in this list is the preferred algorithm.  Any password using different algorithms will be converted
    # automatically upon login.
    root_settings['PASSWORD_HASHERS'] = [
        'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    ]
