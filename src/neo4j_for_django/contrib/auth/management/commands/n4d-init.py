from neo4j_for_django.contrib.auth.node_models import Permission
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    args = ''
    help = """
            Initialize the neo4j_for_django native permissions.
            """

    def handle(self, *args, **options):

        # Initial permissions :
        permissions_dict = {
            "create": "Permission(codename='create', description='The user can create an User instance.')",
            "view_user": "Permission(codename='view_user', description='The user can view an User instance.')",
            "update_user": "Permission(codename='update_user', description='The user can update an User instance.')",
            "delete_user": "Permission(codename='delete_user', description='The user can delete an User instance.')",

            "create_group": "Permission(codename='create_group', description='The user can create a Group instance.')",
            "view_group": "Permission(codename='view_group', description='The user can view a Group instance.')",
            "update_group": "Permission(codename='update_group', description='The user can update a Group instance.')",
            "delete_group": "Permission(codename='delete_group', description='The user can delete a Group instance.')",

            "create_permission": "Permission(codename='create_permission', description='The user can create a Permission instance.')",
            "view_permission": "Permission(codename='view_permission', description='The user can view a Permission instance.')",
            "update_permission": "Permission(codename='update_permission', description='The user can update a Permission instance.')",
            "delete_permission": "Permission(codename='delete_permission', description='The user can delete a Permission instance.')",
        }

        print("\n-----------------------------------")
        print("     Start of initialization")
        print("-----------------------------------")

        for permission_name, permission in permissions_dict.items():
            p = Permission.get(permission_name)
            if p is None:
                eval(permission)
                print(f"✔   '{permission_name}' has been created in the database.")

            else:
                print(f"❌   '{permission_name}' was already created.")

        print("--------------------------------")
        print("     End of initialization")
        print("--------------------------------\n")


