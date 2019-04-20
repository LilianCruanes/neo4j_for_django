from neo4j_for_django.db.base import gdbh
from neo4j_for_django.contrib.sessions.exceptions import N4DSessionDoesNotExist, N4DSessionDoesNotHaveData
from neo4j_for_django.db import node_models
from django.utils import timezone


class AbstractBaseSession:

    def encode(self, session_dict):
        """
        Return the given session dictionary serialized and encoded as a string.
        """
        session_store_class = self.__class__.get_session_store_class()
        return session_store_class().encode(session_dict)

    def save(self, session_key, session_dict, expire_date):
        print("AbstractUser.save() == ", session_key, session_dict, expire_date)

        if session_dict:
            s = self.__class__(session_key, self.encode(session_dict), expire_date)
        else:
            raise N4DSessionDoesNotHaveData("The does'nt have datas ('session_dict'), failed to save it.")
        return s

    def __str__(self):
        return self.session_key

    @classmethod
    def get_session_store_class(cls):
        raise NotImplementedError

    def get_decoded(self):
        session_store_class = self.get_session_store_class()
        return session_store_class().decode(self.session_data)


class Session(node_models.Node, AbstractBaseSession):
    """
    Django provides full support for anonymous sessions. The session
    framework lets you store and retrieve arbitrary data on a
    per-site-visitor basis. It stores data on the server side and
    abstracts the sending and receiving of cookies. Cookies contain a
    session ID -- not the data itself.

    The Django sessions framework is entirely cookie-based. It does
    not fall back to putting session IDs in URLs. This is an intentional
    design decision. Not only does that behavior make URLs ugly, it makes
    your site vulnerable to session-ID theft via the "Referer" header.

    For complete documentation on using Sessions in your code, consult
    the sessions documentation that is shipped with Django (also available
    on the Django Web site).
    """

    labels = "Session"

    _session_key = node_models.Property(key="session_key",
                                        required=True,
                                        unique=True)  # TODO : add max_length = 40
    _session_data = node_models.Property(key='session_data')
    _expire_date = node_models.Property(key='expire_date')  # TODO : add db_index = True

    def __str__(self):
        return f'<Session object(session_key="{self.session_key}", expire_date="{self.expire_date}")>'

    def __repr__(self):
        return f'<Session object(session_key="{self.session_key}", expire_date="{self.expire_date}")>'

    @classmethod
    def get_session_store_class(cls):
        from neo4j_for_django.contrib.sessions.backends.db import SessionStore
        return SessionStore

    @classmethod
    def get(cls, session_key):
        response = gdbh.r_transaction("MATCH (s:Session {session_key:'%s'}) RETURN (s)" % session_key)
        if response:
            return response
        else:
            raise N4DSessionDoesNotExist(f"No Session found with session_key = '{session_key}'.")

    @classmethod
    def exists(cls, session_key):
        try:
            cls.get(session_key)

        except N4DSessionDoesNotExist:
            return False

        else:
            return True

    @classmethod
    def delete(cls, session_key):
        try:
            cls.get(session_key)

        except N4DSessionDoesNotExist:
            raise

        else:
            gdbh.w_transaction("MATCH (s:Session {session_key:'%s'}) DETACH DELETE (s)" % session_key)

    @classmethod
    def clear_expired_sessions(cls):
        gdbh.r_transaction("""
            MATCH (s:Session) 
            WHERE s.expire_date < datetime('%s') 
            DETACH DELETE (s)
            """ % str(timezone.now()).replace(' ', 'T'))
