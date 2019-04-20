from neo4j_for_django.contrib.auth.node_models import User, AnonymousUser
from neo4j_for_django.contrib.auth.exceptions import N4DLoginError
from neo4j_for_django.contrib.auth.hashers import _check_password
from neo4j_for_django.db.base import gdbh
from django.conf import settings


def authenticate(email, password):
    user = User.get(email=email)
    if not isinstance(user, AnonymousUser):
        if _check_password(password, user.password):
            if user.is_active_user:
                return user

    return AnonymousUser()


def _login_user(request, user):
    request.session['logged_user_uuid'] = user.uuid
    request.session.save()

    request.user = user

    gdbh.w_transaction("""
        MATCH (u:User {uuid: '%s'}), (s:Session {session_key: '%s'})
        CREATE (s)-[:IS_SESSION_OF]->(u)
        """ % (user.uuid, request.session.session_key))


def preserve_or_login(request, if_authentication_user=AnonymousUser()):
    from_authentication_user = AnonymousUser()
    from_request_user = AnonymousUser()

    try:
        if not isinstance(if_authentication_user, AnonymousUser):
            if isinstance(if_authentication_user, User):
                from_authentication_user = if_authentication_user

        if not isinstance(request.user, AnonymousUser):
            if isinstance(request.user, User):
                from_request_user = request.user

        if not if_authentication_user and not request.user:
            raise N4DLoginError("To login an user with the 'preserve_or_login()' function, you must provide as function's parameters : the request and the user object.")

    except N4DLoginError:
        request.session.flush()
        raise

    else:
        # If the function is called during an authentication, to login an user :
        if not isinstance(from_authentication_user, AnonymousUser):


            # If the user is not an AnonymousUser and if a 'logged_user_uuid' is already in the session (if the
            # user try to login although it is MAYBE already) :
            if 'logged_user_uuid' in request.session:

                if not isinstance(from_request_user, AnonymousUser) and request.session['logged_user_uuid'] is not None:

                    # If the user is the same in database and session :
                    if from_request_user.uuid == from_authentication_user.uuid == request.session['logged_user_uuid']:
                        current_user_session = from_authentication_user.get_session()

                        # If the session is the same in database and in cookie :
                        if current_user_session and request.session.session_key \
                                and current_user_session.session_key == request.session.session_key:

                            # If settings.N4D_SESSION_CHANGE_ON_EVERY_REQUEST is True, delete and create a new session
                            # Else, just preserve the current session.
                            if settings.N4D_SESSION_CHANGE_ON_EVERY_REQUEST:
                                force_clear_user_session(request)
                                _login_user(request, from_authentication_user)

                        # If the sessions datas are not identical
                        else:
                            force_clear_user_session(request)
                            _login_user(request, from_authentication_user)

                    # If the users datas are not identical
                    else:
                        force_clear_user_session(request)
                        _login_user(request, from_authentication_user)

                # Else if the user is not already logged in :
                else:
                    force_clear_user_session(request)
                    _login_user(request, from_authentication_user)

            else:
                force_clear_user_session(request)
                _login_user(request, from_authentication_user)

        # If the user is not provided during authentication (he is the currently logged user stored in request.user)
        elif not isinstance(from_request_user, AnonymousUser):

            # If a 'logged_user_uuid' is already in the session (if the user is MAYBE already logged) :
            if 'logged_user_uuid' in request.session:

                if request.session['logged_user_uuid'] is not None:

                    # If the user is the same in database and session :
                    if from_request_user.uuid == request.session['logged_user_uuid']:
                        current_user_session = from_request_user.get_session()

                        # If the session is the same in database and in cookie :
                        if current_user_session and request.session.session_key \
                                and current_user_session.session_key == request.session.session_key:

                            # If settings.N4D_SESSION_CHANGE_ON_EVERY_REQUEST is True, delete and create a new session
                            # Else, just preserve the current session.
                            if settings.N4D_SESSION_CHANGE_ON_EVERY_REQUEST:
                                force_clear_user_session(request, from_request_user)
                                _login_user(request, from_request_user)

                        # If the sessions datas are not identical
                        else:
                            force_clear_user_session(request, from_request_user)

                    # If the users datas are not identical
                    else:
                        force_clear_user_session(request, from_request_user)

                # Else if the user is not already logged in :
                else:
                    force_clear_user_session(request, from_request_user)

            else:
                force_clear_user_session(request, from_request_user)

        else:
            request.session.flush()


# Logout function : clear the sessions stored in the cookie and in the database + set request.user with an instance
# of AnonymousUsers
def force_clear_user_session(request):
    gdbh.w_transaction("""
        MATCH (:User {uuid: '%s'})<-[:IS_SESSION_OF]-(s:Session)
        DETACH DELETE (s)
        """ % (request.user.uuid))

    request.session.flush()
    request.user = AnonymousUser()
    request.session.setdefault('logged_user_uuid', None)


def get_user_model():
    return User


# Return the user from the request, if there is'nt, return an instance of AnonymousUser
def get_user_from_request(request):
    if 'logged_user_uuid' in request.session:

        if request.session['logged_user_uuid'] is not None:
            logged_user_uuid = request.session['logged_user_uuid']

            if logged_user_uuid is not None:

                logged_user = User.get(uuid=logged_user_uuid)

                if not isinstance(logged_user, AnonymousUser):
                    return logged_user

                else:
                    # If the user does not exist, clear the session datas, that has nothing to do here
                    request.session.flush()
                    return AnonymousUser()

            else:
                request.session.flush()
                return AnonymousUser()

        else:
            request.session.flush()
            return AnonymousUser()

    else:
        request.session.flush()
        return AnonymousUser()


# Return True if an user is logged, else return False
def get_user_is_logged(request):
    if not isinstance(request.user, AnonymousUser):

        current_user_session = request.user.get_session()
        if current_user_session is not None:

            if request.session:

                if "logged_user_uuid" in request.session:

                    logged_user_uuid = request.session['logged_user_uuid']
                    if logged_user_uuid is not None:

                        if request.user.uuid == logged_user_uuid and \
                                request.session.session_key == current_user_session.session_key:

                            return True
    return False

