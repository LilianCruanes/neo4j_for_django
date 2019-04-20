from neo4j_for_django.db.node_models import Node
from neo4j_for_django.db.base import gdbh
from neo4j_for_django.db.exceptions import N4DNodeLabelsInitializationError
from django.core.management.base import BaseCommand
from test_project.settings import BASE_DIR
import importlib.util
import os


class Command(BaseCommand):
    args = ''
    help = """
            Apply constraints of node models properties.
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
            node_classes = []
            for k, v in node_models.__dict__.items():
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
                    # beginning CONSOLE RENDER PART 4 #
                    print(f"                    - {node_class_name}")
                    # end CONSOLE RENDER PART 4 #

                    # Get needed datas (labels and properties) and format the labels dict into cypher format
                    node_class_labels_list = node_class.get_labels()
                    node_class_labels_cypher_format = self.format_labels_to_cypher(node_class_labels_list, node_class_name)
                    node_class_properties = node_class._get_properties_fields()

                    # For each property of the current node class
                    for property_name, property_content in node_class_properties.items():

                        # If the property is defined as "required" (required=True), create REQUIRED constraint in the database
                        if property_content.required:
                            gdbh.w_transaction("""
                                CREATE CONSTRAINT ON (x:%s) 
                                ASSERT exists(x.%s)
                                """ % (node_class_labels_cypher_format, property_content.key))

                            # beginning CONSOLE RENDER PART 5 #
                            print(f"                        ✔   Apply REQUIRED constraint on '{property_content.key}'.")
                            # end CONSOLE RENDER PART 5 #

                        # If the property is defined as "unique" (unique=True), create UNIQUE constraint in the database
                        if property_content.unique:
                            gdbh.w_transaction("""
                                CREATE CONSTRAINT ON (x:%s)
                                ASSERT x.%s IS UNIQUE
                                """ % (node_class_labels_cypher_format, property_content.key))

                            # beginning CONSOLE RENDER PART 6 #
                            print(f"                        ✔   Apply UNIQUE constraint on '{property_content.key}'.")
                            # end CONSOLE RENDER PART 6 #

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

    @staticmethod
    # Convert dict format to a cypher labels format
    def format_labels_to_cypher(labels_list, label_class_name):
        render = []

        if not labels_list or labels_list is None:
            return label_class_name

        else:
            if isinstance(labels_list, list):
                for label in labels_list:
                    render.append(label)
                return ':'.join(render)

            else:
                raise N4DNodeLabelsInitializationError('self.labels attribute must be a list.')