import os
import importlib.util
import importlib.resources
from django.core.management.base import BaseCommand
from test_project.settings import BASE_DIR
from neo4j_for_django.db.node_models import Node
from neo4j_for_django.contrib.auth.node_models import Permission


class Command(BaseCommand):
    args = ''
    help = """
            Create in the database all the 4 CRUD permissions for all node models in the project.
            """

    def handle(self, *args, **options):
        # beginning CONSOLE RENDER PART 1 #
        print("\n--------------------------------------\n")

        found_path_number = len(self.get_all_node_models_files_path())

        if found_path_number == 1:
            print(f"    {len(self.get_all_node_models_files_path())} 'node_models.py' file has been found :")

        if found_path_number > 1:
            print(f"    {len(self.get_all_node_models_files_path())} 'node_models.py' files have been found :")

        else:
            print(f"    No one file named 'node_models.py' has been found in this django project.")
        # end CONSOLE RENDER PART 1 #

        # For each path of the node_models.py files :
        for path in self.get_all_node_models_files_path():

            # beginning CONSOLE RENDER PART 2 #
            print(f"\n        -> '{path}' :")
            # end CONSOLE RENDER PART 2 #

            # Import the module from his path
            spec = importlib.util.spec_from_file_location("node_models", path)
            node_models = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(node_models)

            # Get all the module classes that have in their parents the Node class.
            node_model_dict = node_models.__dict__
            node_classes = []
            for k, v in node_model_dict.items():
                try:
                    if Node in v.__mro__:
                        node_classes.append(v)
                except:
                    pass
            # beginning CONSOLE RENDER PART 3 #
            if len(node_classes) == 1:
                print(f"                1 node class named has been found : ")

            elif len(node_classes) > 1:
                print(f"                {len(node_classes)} node classes have been found : ")

            else:
                print(f"                No one node class (inherting from Node) has been found.")
            # end CONSOLE RENDER PART 3 #

            # For each node class in the current module node classes :
            for node_class in node_classes:
                node_class_name = node_class.__name__

                # Explanation : __module__ return only the name of the module where is contained the node_class (here :
                # "node_models"), but if the node_class is an import, __module__ return the full module path (example :
                # "neo4j_for_django.contrib.sessions.node_models"). So, this line prevent the detection of the imported
                # classes in the node_models files.
                if node_class.__module__ == "node_models":
                    if node_class_name in ["User", "Permission", "Group"]:
                        print(f"                    - ! ({node_class_name})")
                        print(f"                        ❌   Please, use the 'n4d-init' command to apply the neo4j_for_django natives node models (Permission, Group and User)")
                    else:

                        # beginning CONSOLE RENDER PART 4 #
                        print(f"                    - {node_class_name}")
                        # end CONSOLE RENDER PART 4 #

                        # Check if the "create" permission is already in the database.
                        create_permission = Permission.get("create_" + str(node_class_name).lower())

                        # If there is'nt create it :
                        if create_permission is None:
                            Permission(codename="create_" + str(node_class_name).lower(),
                                       description=f"The user can create {str(node_class_name)} nodes.")
                            print(f"                        ✔   Create a 'create' permission.")

                        else:
                            print(f"                        ❌   'create' permission was already created.")

                        # Check if the "view" permission is already in the database.
                        view_permission = Permission.get("view_" + str(node_class_name).lower())

                        # If there is'nt create it :
                        if view_permission is None:
                            Permission(codename="view_" + str(node_class_name).lower(),
                                       description=f"The user can view {str(node_class_name)} nodes.")
                            print(f"                        ✔   Create a 'view' permission.")

                        else:
                            print(f"                        ❌   'view' permission was already created.")

                        # Check if the "update" permission is already in the database.
                        update_permission = Permission.get("update_" + str(node_class_name).lower())

                        # If there is'nt create it :
                        if update_permission is None:
                            Permission(codename="update_" + str(node_class_name).lower(),
                                       description=f"The user can update {str(node_class_name)} nodes.")
                            print(f"                        ✔   Create an 'update' permission.")

                        else:
                            print(f"                        ❌   'update' permission was already created.")

                        # Check if the "delete" permission is already in the database.
                        delete_permission = Permission.get("delete_" + str(node_class_name).lower())

                        # If there is'nt create it :
                        if delete_permission is None:
                            Permission(codename="delete_" + str(node_class_name).lower(),
                                       description=f"The user can delete {str(node_class_name)} nodes.")
                            print(f"                        ✔   Create a 'delete' permission.")

                        else:
                            print(f"                        ❌   'delete' permission was already created.")

        # beginning CONSOLE RENDER PART 7 #
        print("\n--------------------------------------\n")
        # end CONSOLE RENDER PART 7 #

    # This function return a list of paths of node models files (contained in the current django project)
    @staticmethod
    def get_all_node_models_files_path():
        result = []
        for root, dirs, files in os.walk(BASE_DIR):
            if 'node_models.py' in files:
                result.append(os.path.join(root, 'node_models.py'))

        return result