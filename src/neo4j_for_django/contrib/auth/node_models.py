from neo4j_for_django.db import node_models
from neo4j_for_django.db.base import gdbh
from neo4j_for_django.contrib.auth.exceptions import *
from neo4j_for_django.db.utils import make_uuid
from neo4j_for_django.contrib.auth.hashers import _hash_password
from neo4j_for_django.contrib.sessions.node_models import Session
import datetime
import warnings


class FakeClass:
    pass


class Permission(node_models.Node):
    labels = 'Permission'

    _codename = node_models.Property(key='codename',
                                     unique=True,
                                     required=True)

    _description = node_models.Property(key='description',
                                        unique=True,
                                        required=True)

    def __str__(self):
        return f'<Permission object(codename="{self.codename}", description="{self.description}")>'

    def __repr__(self):
        return f'<Permission object(codename="{self.codename}", description="{self.description}")>'

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            if self.codename == other.codename and self.description == other.description:
                return True
            else:
                return False
        else:
            raise NotImplemented("These different types elements cannot be compared")

    def __hash__(self):
        return hash(self.codename) + hash(self.description)

    @classmethod
    def get(cls, permission_codename):
        response = gdbh.r_transaction('MATCH (p:Permission {codename:"%s"}) RETURN (p)' % permission_codename)

        if response:
            fake_permission_instance = FakeClass()
            fake_permission_instance.__class__ = cls
            setattr(fake_permission_instance, 'description', response[0]['p']._properties['description'])
            setattr(fake_permission_instance, 'codename', response[0]['p']._properties['codename'])

            return fake_permission_instance

        else:
            return None


class Group(node_models.Node):
    labels = 'Group'

    _uuid = node_models.Property(key='uuid',
                                 default=make_uuid,
                                 unique=True)

    _name = node_models.Property(key='name',
                                 unique=True,
                                 required=True)

    def __str__(self):
        return f'<Group object(name="{self.name}", uuid="{self.uuid}")>'

    def __repr__(self):
        return f'<Group object(name="{self.name}", uuid="{self.uuid}")>'

    @classmethod
    def get(cls, group_name):
        response = gdbh.r_transaction("MATCH (g:Group {name: '%s'}) RETURN (g)" % group_name)

        if response:
            fake_permission_instance = FakeClass()
            fake_permission_instance.__class__ = cls
            setattr(fake_permission_instance, 'uuid', response[0]['g']._properties['uuid'])
            setattr(fake_permission_instance, 'name', response[0]['g']._properties['name'])

            return fake_permission_instance

        else:
            return None

    def get_permissions(self):
        request_response = gdbh.r_transaction("""
            MATCH (:Group {uuid:'%s'})-[:CAN]->(p:Permission)
            RETURN (p)
            """ % self.uuid)

        if request_response:

            render = set()

            for permission in request_response:
                fake_permission_instance = FakeClass()
                fake_permission_instance.__class__ = Permission
                setattr(fake_permission_instance, 'description', permission['p']._properties['description'])
                setattr(fake_permission_instance, 'codename', permission['p']._properties['codename'])
                render.add(fake_permission_instance)

            if render:
                return render

        return None

    def get_users(self):
        request_response = gdbh.r_transaction("""
                    MATCH (u:User)-[:IS_IN]->(:Group {uuid:'%s'})
                    RETURN u
                    """ % self.uuid)

        if request_response:

            render = set()

            for user in request_response:
                fake_user_instance = FakeClass()
                fake_user_instance.__class__ = User
                setattr(fake_user_instance, 'is_super_user', user['u']._properties['is_super_user'])
                setattr(fake_user_instance, 'is_staff_user', user['u']._properties['is_staff_user'])
                setattr(fake_user_instance, 'is_active_user', user['u']._properties['is_active_user'])
                setattr(fake_user_instance, 'uuid', user['u']._properties['uuid'])
                setattr(fake_user_instance, 'first_name', user['u']._properties['first_name'])
                setattr(fake_user_instance, 'last_name', user['u']._properties['last_name'])
                setattr(fake_user_instance, 'email', user['u']._properties['email'])
                setattr(fake_user_instance, 'password', user['u']._properties['password'])
                setattr(fake_user_instance, 'registration_datetime', user['u']._properties['registration_datetime'])

                render.add(fake_user_instance)

            if render:
                return render

        return None

    def add_permission(self, permission_code_name):
        try:
            Permission.get(permission_code_name)

        except N4DPermissionDoesNotExist:
            raise

        else:
            gdbh.w_transaction("""
                MATCH (p:Permission {codename:'%s'})
                MATCH (g:Group {uuid:'%s'})
                CREATE (g)-[:CAN]->(p)
                """ % (permission_code_name, self.uuid))


class User(node_models.Node):
    labels = 'User'

    # Default groups
    _is_super_user = node_models.Property(key='is_super_user',
                                          default=False)
    _is_staff_user = node_models.Property(key='is_staff_user',
                                          default=False)
    _is_active_user = node_models.Property(key='is_active_user',
                                           default=True)

    _uuid = node_models.Property(key='uuid',
                                 default=make_uuid,
                                 unique=True)

    _first_name = node_models.Property(key='first_name',
                                       required=True)

    _last_name = node_models.Property(key='last_name',
                                      required=True)

    _email = node_models.Property(key='email',
                                  required=True,
                                  unique=True)

    _password = node_models.Property(key='password',
                                     required=True)

    _registration_datetime = node_models.Property(key='registration_datetime',
                                                  default=datetime.datetime.now)  # TODO: Replace by timezone.now

    def __str__(self):
        return f'<User object(first_name="{self.first_name}", last_name="{self.last_name}", uuid="{self.uuid}")>'

    def __repr__(self):
        return f'<User object(first_name="{self.first_name}", last_name="{self.last_name}", uuid="{self.uuid}")>'

    @classmethod
    def create(cls, **extrafields):
        extrafields.setdefault('is_super_user', False)
        extrafields.setdefault('is_staff_user', False)
        extrafields.setdefault('is_active_user', True)

        extrafields['password'] = _hash_password(extrafields['password'])

        new_user = User(**extrafields)

        return new_user

    @classmethod
    def create_super_user(cls, **extrafields):
        extrafields.setdefault('is_super_user', True)
        extrafields.setdefault('is_staff_user', True)
        extrafields.setdefault('is_active_user', True)

        extrafields['password'] = _hash_password(extrafields['password'])

        is_super_user = extrafields.get('is_super_user')
        is_staff_user = extrafields.get('is_staff_user')
        if not is_super_user:
            raise ValueError('A SuperUser must have "is_super_user = True".')

        elif not is_staff_user:
            raise ValueError('A SuperUser must have "is_staff_user = True".')

        else:
            new_super_user = User(**extrafields)

            return new_super_user

    @classmethod
    def get(cls, uuid=None, email=None):

        if uuid and email is None:
            properties = f"uuid: '{uuid}'"

        elif email and uuid is None:
            properties = f"email: '{email}'"

        elif uuid and email:
            properties = f"uuid: '{uuid}', email: '{email}'"

        else:
            raise N4DGetUserError("To get an user, you must provide his 'uuid' or his 'email' or both.")

        response = gdbh.r_transaction("MATCH (u:User {%s}) RETURN (u)" % properties)

        if response:
            fake_user_instance = FakeClass()
            fake_user_instance.__class__ = cls
            setattr(fake_user_instance, 'is_super_user', response[0]['u']._properties['is_super_user'])
            setattr(fake_user_instance, 'is_staff_user', response[0]['u']._properties['is_staff_user'])
            setattr(fake_user_instance, 'is_active_user', response[0]['u']._properties['is_active_user'])
            setattr(fake_user_instance, 'uuid', response[0]['u']._properties['uuid'])
            setattr(fake_user_instance, 'first_name', response[0]['u']._properties['first_name'])
            setattr(fake_user_instance, 'last_name', response[0]['u']._properties['last_name'])
            setattr(fake_user_instance, 'email', response[0]['u']._properties['email'])
            setattr(fake_user_instance, 'password', response[0]['u']._properties['password'])
            setattr(fake_user_instance, 'registration_datetime', response[0]['u']._properties['registration_datetime'])

            return fake_user_instance

        else:
            return AnonymousUser()

    def update(self, user_property, new_user_property_value):
        if user_property not in self.__dict__.keys():
            warnings.warn(
                f"WARNING : You try to update the property '{user_property}' of an user, but this property was not found in the user dict. The update will have maybe no effect.",
                N4DUserPropertyWarning)

        if isinstance(new_user_property_value, int) or isinstance(new_user_property_value, bool):
            gdbh.w_transaction("""
                MATCH (u:User {uuid:'%s'})
                WHERE exists(u.%s)
                SET u.%s = %s
                """ % (self.uuid, user_property, user_property, new_user_property_value))

        else:
            gdbh.w_transaction("""
                MATCH (u:User {uuid:'%s'})
                WHERE exists(u.%s)
                SET u.%s = '%s'
                """ % (self.uuid, user_property, user_property, new_user_property_value))

        setattr(self, user_property, new_user_property_value)

    def _get_only_user_permissions(self):
        request_response = gdbh.r_transaction("""
            MATCH (:User {uuid:'%s'})-[:CAN]->(p:Permission)
            RETURN p
            """ % self.uuid)

        if request_response:
            render = set()

            for permission in request_response:
                fake_permission_instance = FakeClass()
                fake_permission_instance.__class__ = Permission
                setattr(fake_permission_instance, 'description', permission['p']._properties['description'])
                setattr(fake_permission_instance, 'codename', permission['p']._properties['codename'])
                render.add(fake_permission_instance)

            if render:
                return render

        return None

    def get_permissions(self):
        if self.is_active_user:
            render = set()
            only_user_permissions = self._get_only_user_permissions()
            user_groups = self.get_groups()

            if only_user_permissions:
                for user_only_permission in only_user_permissions:
                    render.add(user_only_permission)

            if user_groups:
                for group in user_groups:
                    for group_permission in group.get_group_permissions():
                        render.add(group_permission)

            if render:
                return render

        return None

    def get_groups(self):
        request_response = gdbh.r_transaction("""
            MATCH (:User {uuid:'%s'})-[:IS_IN]->(g:Group)
            RETURN (g)
            """ % self.uuid)

        if request_response:
            render = set()

            for group in request_response:
                fake_group_instance = FakeClass()
                fake_group_instance.__class__ = Group
                setattr(fake_group_instance, 'uuid', group['g']._properties['uuid'])
                setattr(fake_group_instance, 'name', group['g']._properties['name'])
                render.add(fake_group_instance)

            if render:
                return render

        return None

    def get_session(self):
        response = gdbh.r_transaction("""
            MATCH (:User {uuid:'%s'})<-[:IS_SESSION_OF]-(s:Session)
            RETURN (s)
            """ % self.uuid)

        if response:
            fake_session_instance = FakeClass()
            fake_session_instance.__class__ = Session

            try:
                setattr(fake_session_instance, 'session_key', response[0]['s']._properties['session_key'])
                setattr(fake_session_instance, 'session_data', response[0]['s']._properties['session_data'])
                setattr(fake_session_instance, 'expire_date', response[0]['s']._properties['expire_date'])

            except AttributeError:  # If ne session isn't stored, it will not have attribute 'properties'.
                return None

            else:
                return fake_session_instance

        else:
            return None

    def add_permission(self, permission_code_name):
        try:
            Permission.get(permission_code_name)

        except N4DPermissionDoesNotExist:
            raise

        else:
            gdbh.w_transaction("""
                MATCH (p:Permission {codename:'%s'})
                MATCH (u:User {uuid:'%s'})
                CREATE (u)-[:CAN]->(p) 
                """ % (permission_code_name, self.uuid))

    def add_group(self, group_name):
        if isinstance(group_name, str):
            try:
                Group.get(group_name)

            except N4DGroupDoesNotExist:
                raise

            else:
                gdbh.w_transaction("""
                    MATCH (g:Group {name:'%s'}), (p:User {uuid:'%s'})
                    CREATE (p)-[:IS_IN]->(g)
                    """ % (group_name, self.uuid))

    def has_perm(self, permission_code_name):
        if self.is_super_user:
            return True
        if not self.is_active_user:
            return False
        else:
            permission_to_test = Permission.get(permission_code_name)
            all_user_permissions = self.get_permissions()
            if all_user_permissions is not None:
                if permission_to_test in all_user_permissions:
                    return True
            return False


class AnonymousUser:
    is_super_user = False
    is_staff_user = False
    is_active_user = False
    uuid = None
    first_name = None
    last_name = None
    email = None
    password = None
    registration_datetime = None
    _self_permissions = None

    def __str__(self):
        return 'AnonymousUser'

    def __repr__(self):
        return 'AnonymousUser'

    @classmethod
    def create_user(cls, **extrafields):
        raise NotImplementedError("neo4j_for_django doesn't provide a DB representation for AnonymousUser.")

    @classmethod
    def create_super_user(cls, **extrafields):
        raise NotImplementedError("neo4j_for_django doesn't provide a DB representation for AnonymousUser.")

    @classmethod
    def get(cls):
        return cls()

    def update(self, user_property, new_user_property_value):
        raise NotImplementedError("neo4j_for_django doesn't provide a DB representation for AnonymousUser.")

    def get_groups(self):
        return None

    def _get_only_user_permissions(self):
        return None

    def get_permissions(self):
        return None

    def get_session(self):
        return None

    def add_permission(self, permission_code_name):
        raise NotImplementedError("neo4j_for_django doesn't provide a DB representation for AnonymousUser.")

    def add_group(self, group_name_or_object):
        raise NotImplementedError("neo4j_for_django doesn't provide a DB representation for AnonymousUser.")

    def has_perm(self, permission_code_name):
        return False

